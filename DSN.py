import io
import time
import threading
from tkinter import *
from tkinter.messagebox import showinfo
import sys
import grpc
from PIL import Image, ImageTk
from resources.LaunchVehicle_pb2 import LaunchVehicle_pb2_grpc, LaunchVehicle_pb2
from resources.Payload_pb2 import Payload_pb2, Payload_pb2_grpc
import servers


class DSN(Tk):
    def __init__(self):
        super().__init__()
        self.title("Space Z Deep Space Network")
        self.geometry("600x600+50+50")
        self.all_vehicles, self.vehicles, self.payloads = servers.populate_vehicles_and_payloads()
        self.vehicle_names = [vehicle.name for vehicle in self.vehicles]
        self.vehicles_dict = {vehicle.name: vehicle for vehicle in self.all_vehicles}
        self.payloads_dict = {payload.name: payload for payload in self.payloads}
        self.options = StringVar(value=self.vehicle_names)
        self.active_vehicles = []
        self.active_payloads = []
        self.vehicle_windows = {vehicle.name: None for vehicle in self.vehicles}
        self.payload_windows = {payload.name: None for payload in self.payloads}

        Label(self, text="Spacecraft Ready For Launch").pack(pady=10)
        self.launch_listbox = Listbox(self, listvariable=self.options, height=5, exportselection=False)
        self.launch_listbox.select_set(0)
        self.launch_listbox.pack()
        self.launch_button = Button(self, text='Click to Interact with Launch Vehicle', command=self.vehicle_launch_window)
        self.launch_button.pack()

        Label(self, text="Active Spacecraft").pack(pady=10)
        self.active_vehicles_listbox = Listbox(self, listvariable=self.active_vehicles, height=5, exportselection=False)
        self.active_vehicles_listbox.pack()
        self.active_vehicles_button = Button(self, text='Click for Vehicle Details', state='disabled', command=self.resume_window)
        self.active_vehicles_button.pack()

        Label(self, text="Active Payloads").pack(pady=10)
        self.active_payloads_listbox = Listbox(self, listvariable=self.active_payloads, height=5, exportselection=False)
        self.active_payloads_listbox.pack()
        self.active_payloads_button = Button(self, text='Click for Payload Details', state='disabled', command=self.open_payload_window)
        self.active_payloads_button.pack()

        self.protocol("WM_DELETE_WINDOW", self.destroy_all)

    def vehicle_launch_window(self):
        vehicle_index = self.launch_listbox.curselection()
        vehicle_name = self.launch_listbox.get(vehicle_index)
        VehicleWindow(self, vehicle_index, vehicle_name)

    def resume_window(self):
        vehicle_index = self.active_vehicles_listbox.curselection()
        vehicle_name = self.active_vehicles_listbox.get(vehicle_index)
        self.vehicle_windows[vehicle_name].deiconify()

    def open_payload_window(self):
        vehicle_index = self.active_payloads_listbox.curselection()
        vehicle_name = self.active_payloads_listbox.get(vehicle_index)
        PayloadWindow(self, vehicle_name)

    def destroy_all(self):
        for window in self.vehicle_windows.values():
            if window:
                if window._stop_event and not window._stop_event.is_set():
                    window._stop_event.set()
                window.destroy()

        for window in self.payload_windows.values():
            if window:
                if window._telemetry_stop_event and not window._telemetry_stop_event.is_set():
                    window._telemetry_stop_event.set()
                if window._data_stop_event and not window._data_stop_event.is_set():
                    if window.type == 'Spy':
                        window.stopData()
                        time.sleep(5)
                    else:
                        window._data_stop_event.set()
                window.destroy()
        time.sleep(5)
        self.destroy()


class VehicleWindow(Toplevel):
    def __init__(self, root, vehicle_index, vehicle_name):
        if not root.vehicle_windows[vehicle_name]:
            super().__init__(root)
            self.vehicle = root.vehicles_dict[vehicle_name]
            self.vehicle_index = vehicle_index
            self.stub = LaunchVehicle_pb2_grpc.LaunchVehicleServiceStub(grpc.insecure_channel('localhost:{}'.format(self.vehicle.port)))
            self.title("Launch Vehicle {}".format(self.vehicle.name))
            self.geometry("400x400")
            self.altitude = StringVar(self, self.vehicle.telemetry['altitude'])
            self.latitude = StringVar(self, self.vehicle.telemetry['latitude'])
            self.longitude = StringVar(self, self.vehicle.telemetry['longitude'])
            self.temperature = StringVar(self, self.vehicle.telemetry['temperature'])
            self.timeToOrbit = StringVar(self, self.vehicle.telemetry['timeToOrbit'])
            self.telemetry_thread = None
            self._stop_event = None

            Label(self, text="Altitude").pack()
            altitude_label = Label(self, textvariable=self.altitude)
            altitude_label.pack()

            Label(self, text="Latitude").pack()
            latitude_label = Label(self, textvariable=self.latitude)
            latitude_label.pack()

            Label(self, text="Longitude").pack()
            longitude_label = Label(self, textvariable=self.longitude)
            longitude_label.pack()

            Label(self, text="Temperature").pack()
            temperature_label = Label(self, textvariable=self.temperature)
            temperature_label.pack()

            Label(self, text="Time to Orbit").pack()
            time_to_orbit_label = Label(self, textvariable=self.timeToOrbit)
            time_to_orbit_label.pack()

            self.launch_button = Button(self, text='Launch', command=lambda: self.launch(root))
            self.launch_button.pack()

            self.deploy_button = Button(self, text='Deploy Payload', command=lambda: self.deployPayload(root), state='disabled')
            self.deploy_button.pack()

            self.deorbit_button = Button(self, text='Deorbit', command=lambda: self.deorbit(root), state='disabled')
            self.deorbit_button.pack()

            self.start_telemetry_button = Button(self, text='Start Telemetry', command=self.startTelemetry)
            self.start_telemetry_button.pack()

            self.stop_telemetry_button = Button(self, text='Stop Telemetry', command=self.stopTelemetry, state='disabled')
            self.stop_telemetry_button.pack()

            root.vehicle_windows[vehicle_name] = self
            self.protocol("WM_DELETE_WINDOW", root.vehicle_windows[vehicle_name].withdraw)
        else:
            root.vehicle_windows[vehicle_name].deiconify()

    def launch(self, root):
        self.launch_button['state'] = 'disabled'
        root.active_vehicles_button['state'] = 'normal'
        root.active_vehicles_listbox.insert('end', root.launch_listbox.get(root.launch_listbox.curselection()))
        root.active_vehicles_listbox.select_set(0)
        root.launch_listbox.delete(self.vehicle_index)
        request = LaunchVehicle_pb2.VehicleRequest(vehicleName=self.vehicle.name)
        for response in self.stub.VehicleLaunch(request=request):
            self.timeToOrbit.set(response.timeToOrbit)
            self.update()
        self.deploy_button['state'] = 'normal'
        self.deorbit_button['state'] = 'normal'
        if root.launch_listbox.size() == 0:
            root.launch_button['state'] = 'disabled'
        else:
            root.launch_listbox.select_set(0)
        showinfo(title='Orbit Reached', message='{} has reached orbit!'.format(self.vehicle.name))

    def deployPayload(self, root):
        self.deploy_button['state'] = 'disabled'
        root.active_payloads_listbox.insert('end', self.vehicle.payload.name)
        root.active_payloads_listbox.select_set(0)
        root.active_payloads_button['state'] = 'normal'
        request = LaunchVehicle_pb2.VehicleRequest(vehicleName=self.vehicle.name)
        self.stub.DeployPayload(request=request)
        showinfo(title='Payload Deployed', message='{} Payload {} has been deployed!'.format(self.vehicle.payload.type, self.vehicle.payload.name))

    def deorbit(self, root):
        request = LaunchVehicle_pb2.VehicleRequest(vehicleName=self.vehicle.name)
        if self._stop_event and not self._stop_event.is_set():
            self._stop_event.set()
        time.sleep(1)
        self.stub.Deorbit(request=request)
        active_vehicles_index = root.active_vehicles_listbox.get(0, "end").index(self.vehicle.name)
        root.active_vehicles_listbox.delete(active_vehicles_index)
        self.deorbit_button['state'] = 'disabled'
        self.launch_button['state'] = 'disabled'
        self.start_telemetry_button['state'] = 'disabled'
        self.stop_telemetry_button['state'] = 'disabled'
        self.deploy_button['state'] = 'disabled'
        if root.active_vehicles_listbox.size() == 0:
            root.active_vehicles_button['state'] = 'disabled'
        showinfo(title='Launch Vehicle Deorbited', message='Launch Vehicle {} has deorbited.'.format(self.vehicle.name))

    def startTelemetry(self):
        self.start_telemetry_button['state'] = 'disabled'
        self.stop_telemetry_button['state'] = 'normal'
        self.telemetry_thread = threading.Thread(target=self.stream)
        self._stop_event = threading.Event()
        self.telemetry_thread.start()

    def stream(self):
        request = LaunchVehicle_pb2.VehicleRequest(vehicleName=self.vehicle.name)
        for response in self.stub.VehicleStartTelemetry(request=request):
            if not self._stop_event.is_set():
                self.altitude.set(response.altitude)
                self.latitude.set(response.latitude)
                self.longitude.set(response.longitude)
                self.temperature.set(response.temperature)
                self.update()
            else:
                break

    def stopTelemetry(self):
        self.stop_telemetry_button['state'] = 'disabled'
        self.start_telemetry_button['state'] = 'normal'
        self._stop_event.set()
        self.telemetry_thread = None
        request = LaunchVehicle_pb2.VehicleRequest(vehicleName=self.vehicle.name)
        self.stub.VehicleStopTelemetry(request=request)


class PayloadWindow(Toplevel):
    def __init__(self, root, payload_name):
        if not root.payload_windows[payload_name]:
            super().__init__(root)
            self.payload = root.payloads_dict[payload_name]
            self.type = self.payload.type
            self.stub = Payload_pb2_grpc.PayLoadServiceStub(grpc.insecure_channel('localhost:{}'.format(self.payload.port)))
            self.title("Payload {}".format(self.payload.name))
            self.geometry("400x650")
            self.altitude = StringVar(self, self.payload.telemetry['altitude'])
            self.latitude = StringVar(self, self.payload.telemetry['latitude'])
            self.longitude = StringVar(self, self.payload.telemetry['longitude'])
            self.temperature = StringVar(self, self.payload.telemetry['temperature'])
            self._telemetry_thread = None
            self._telemetry_stop_event = None
            self._data_thread = None
            self._data_stop_event = None
            self.rainfall = StringVar(self, 0)
            self.humidity = StringVar(self, 0)
            self.snow = StringVar(self, 0)
            self.download_speed = StringVar(self, 0)
            self.upload_speed = StringVar(self, 0)
            self.image = ImageTk.PhotoImage(Image.new("RGB", (250, 250), "white"))

            Label(self, text="Payload Type").pack()
            Label(self, text=self.payload.type).pack()

            Label(self, text="Altitude").pack()
            altitude_label = Label(self, textvariable=self.altitude)
            altitude_label.pack()

            Label(self, text="Latitude").pack()
            latitude_label = Label(self, textvariable=self.latitude)
            latitude_label.pack()

            Label(self, text="Longitude").pack()
            longitude_label = Label(self, textvariable=self.longitude)
            longitude_label.pack()

            Label(self, text="Temperature").pack()
            temperature_label = Label(self, textvariable=self.temperature)
            temperature_label.pack()

            self.start_telemetry_button = Button(self, command=self.startTelemetry, text='Start Telemetry')
            self.start_telemetry_button.pack()

            self.stop_telemetry_button = Button(self, command=self.stopTelemetry, text='Stop Telemetry', state='disabled')
            self.stop_telemetry_button.pack()

            self.decommission_button = Button(self, command=lambda: self.decommission(root), text='Decommission')
            self.decommission_button.pack()

            self.start_data_button = Button(self, command=self.startData, text='Start Data')
            self.start_data_button.pack()

            self.stop_data_button = Button(self, command=self.stopData, text='Stop Data', state='disabled')
            self.stop_data_button.pack()

            if(self.payload.type == 'Scientific'):
                Label(self, text="Rainfall (mm)").pack()
                rainfall_label = Label(self, textvariable=self.rainfall)
                rainfall_label.pack()

                Label(self, text="Humidity (%)").pack()
                humidity_label = Label(self, textvariable=self.humidity)
                humidity_label.pack()

                Label(self, text="Snow (in)").pack()
                snow_label = Label(self, textvariable=self.snow)
                snow_label.pack()
            elif(self.payload.type == 'Communication'):
                Label(self, text="Download Speed (Mb/s)").pack()
                download_label = Label(self, textvariable=self.download_speed)
                download_label.pack()

                Label(self, text="Upload Speed (Mb/s)").pack()
                upload_label = Label(self, textvariable=self.upload_speed)
                upload_label.pack()
            else:
                Label(self, text="Image").pack()
                self.image_label = Label(self, image=self.image)
                self.image_label.pack()

            root.payload_windows[payload_name] = self
            self.protocol("WM_DELETE_WINDOW", root.payload_windows[payload_name].withdraw)
        else:
            root.payload_windows[payload_name].deiconify()

    def decommission(self, root):
        request = Payload_pb2.PayloadRequest(vehicleName=self.payload.name)
        if self._telemetry_stop_event and not self._telemetry_stop_event.is_set():
            self._telemetry_stop_event.set()
        if self._data_stop_event and not self._data_stop_event.is_set():
            self._data_stop_event.set()
        time.sleep(3)
        self.stub.Decommission(request=request)
        active_payloads_index = root.active_payloads_listbox.get(0, "end").index(self.payload.name)
        root.active_payloads_listbox.delete(active_payloads_index)
        self.decommission_button['state'] = 'disabled'
        self.start_telemetry_button['state'] = 'disabled'
        self.stop_telemetry_button['state'] = 'disabled'
        self.start_data_button['state'] = 'disabled'
        self.stop_data_button['state'] = 'disabled'
        if root.active_payloads_listbox.size() == 0:
            root.active_payloads_button['state'] = 'disabled'
        showinfo(title='Payload Decommissioned', message='{} Payload {} has been decommissioned.'.format(self.payload.type, self.payload.name))


    def startTelemetry(self):
        self.start_telemetry_button['state'] = 'disabled'
        self.stop_telemetry_button['state'] = 'normal'
        self._telemetry_thread = threading.Thread(target=self.streamTelemetry)
        self._telemetry_stop_event = threading.Event()
        self._telemetry_thread.start()

    def streamTelemetry(self):
        request = Payload_pb2.PayloadRequest(vehicleName=self.payload.name)
        for response in self.stub.PayloadStartTelemetry(request=request):
            if not self._telemetry_stop_event.is_set():
                self.altitude.set(response.altitude)
                self.latitude.set(response.latitude)
                self.longitude.set(response.longitude)
                self.temperature.set(response.temperature)
                self.update()
            else:
                break

    def stopTelemetry(self):
        self.stop_telemetry_button['state'] = 'disabled'
        self.start_telemetry_button['state'] = 'normal'
        self._telemetry_stop_event.set()
        self._telemetry_thread = None
        request = Payload_pb2.PayloadRequest(vehicleName=self.payload.name)
        self.stub.PayloadStopTelemetry(request=request)

    def startData(self):
        self.start_data_button['state'] = 'disabled'
        self.stop_data_button['state'] = 'normal'
        self._data_thread = threading.Thread(target=self.streamData)
        self._data_stop_event = threading.Event()
        self._data_thread.start()

    def streamData(self):
        request = Payload_pb2.PayloadRequest(vehicleName=self.payload.name)
        if self.type == 'Scientific':
            for response in self.stub.StartSciData(request=request):
                if not self._data_stop_event.is_set():
                    self.rainfall.set(response.rainfall)
                    self.humidity.set(response.humidity)
                    self.snow.set(response.snow)
                    self.update()
                else:
                    break
        elif self.type == 'Communication':
            for response in self.stub.StartCommsData(request=request):
                if not self._data_stop_event.is_set():
                    self.download_speed.set(response.downloadSpeed)
                    self.upload_speed.set(response.uploadSpeed)
                    self.update()
                else:
                    break
        else:
            for response in self.stub.StartSpyData(request=request):
                if not self._data_stop_event.is_set():
                    image_data = response.image
                    binary = bytearray(image_data)
                    image = Image.open(io.BytesIO(binary)).resize((250, 250))
                    tk_image = ImageTk.PhotoImage(image)
                    self.image_label.configure(image=tk_image)
                    #self.update()
                else:
                    break

    def stopData(self):
        request = Payload_pb2.PayloadRequest(vehicleName=self.payload.name)
        self.stub.StopData(request=request)
        self.stop_data_button['state'] = 'disabled'
        self.start_data_button['state'] = 'normal'
        self._data_stop_event.set()
        self._data_thread = None



if __name__ == '__main__':
    workers = servers.main()
    app = DSN()
    app.mainloop()
    servers.stop(workers)
    sys.exit(0)

