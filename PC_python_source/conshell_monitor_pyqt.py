import sys
import socket 
import struct
from PyQt5.QtWidgets import *
from PyQt5 import uic

# read ui file
form_class = uic.loadUiType("conshell_ui.ui")[0]

# main window 
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        self.host = '172.31.99.2'
        self.port = 9998
       
        self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
        self.client_socket.connect((self.host, self.port))

        self.askStatus.clicked.connect(self.ask_Status)
        self.doControl.clicked.connect(self.do_control)
        self.systemSet.clicked.connect(self.system_set)
        self.askSystem.clicked.connect(self.ask_system)
        
        self.edt_set_project_id.textChanged.connect(self.set_project_id)
        self.edt_set_project_name.textChanged.connect(self.set_project_name)
        self.edt_set_cage_id.textChanged.connect(self.set_cage_id)
        self.edt_set_start_time.textChanged.connect(self.set_start_time)
        self.edt_set_stop_time.textChanged.connect(self.set_stop_time)
        self.edt_set_calc_rate.textChanged.connect(self.set_calc_rate)

        self.edt_d_sensor_no.textChanged.connect(self.set_d_sensor_no)
        self.edt_d_sensor_var.textChanged.connect(self.set_d_sensor_var)

        self.ProjectID = 0x00
        self.ProjectName = b''
        self.CageID = 0x00
        self.autoInterval = 0x00
        self.distCalcRate = 0x00
        self.startLab_y = 2021 
        self.startLab_mo = 4
        self.startLab_d = 28 
        self.startLab_h = 12 
        self.startLab_mi = 30 
        self.startLab_s = 0 
        self.stopLab_y = 2021 
        self.stopLab_mo = 4
        self.stopLab_d = 28 
        self.stopLab_h = 12 
        self.stopLab_mi = 30 
        self.stopLab_s = 0 

        self.d_sensor_no = 0
        self.d_sensor_value = 0

    def set_project_id(self):
        try:
            print(self.edt_set_project_id.text())
            self.ProjectID = int(self.edt_set_project_id.text())
        except ValueError:
            pass

    def set_project_name(self):
        print(self.edt_set_project_name.text())
        self.ProjectName = str.encode(self.edt_set_project_name.text())

    def set_cage_id(self):
        try:
            print(self.edt_set_cage_id.text())
            self.CageID = int(self.edt_set_cage_id.text())
        except ValueError:
            pass

    def set_start_time(self):
        print(self.edt_set_start_time.text())

    def set_stop_time(self):
        print(self.edt_set_stop_time.text())

    def set_calc_rate(self):
        try:
            print(self.edt_set_calc_rate.text())
            self.distCalcRate = float(self.edt_set_calc_rate.text())
        except ValueError:
            pass

    def set_auto_inter(self):
        try:
            print(self.edt_set_calc_rate.text())
            self.autoInterval = int(self.edt_set_calc_rate.text())
        except ValueError:
            pass

    def set_d_sensor_no(self):
        try:
            print(self.edt_d_sensor_no.text())
            self.d_sensor_no = int(self.edt_d_sensor_no.text())
        except ValueError:
            pass

    def set_d_sensor_var(self):
        try:
            print(self.edt_d_sensor_var.text())
            self.d_sensor_var = int(self.edt_d_sensor_var.text())
        except ValueError:
            pass
    

    # ask status button 
    def ask_Status(self) :
        # packet  
        STX = 0x0203
        CMD = 0x51
        dummy = 0xff
        mode = 0x00
        result = 0x00
        CRC = 0xffff
        len = 0x00
        # pack packet and send packet 
        value = (STX, CMD, dummy, mode, result, CRC, len)
        fmt = '>H B B B B H B'.format()
        packer = struct.Struct(fmt)
        cmd = packer.pack(*value)
        self.client_socket.send(cmd) 
        # receive data 
        data = self.client_socket.recv(1024)
        fmt = '>H B B B B H B H H B I f H H I H H I H H f f f I I I I I I I I I I I I I I B B B B B B B B B B B B B B B B B'.format()
        unpack_data = struct.unpack(fmt, data)
        print(unpack_data)
        self.label_prj_id_var.setText(str(unpack_data[7]))
        self.label_cage_id_var.setText(str(unpack_data[8]))
        self.label_rat_temp_var.setText(str(unpack_data[11]))
        self.label_x_var.setText(str(unpack_data[12]))
        self.label_y_var.setText(str(unpack_data[13]))
        self.labelA2_RatWeight_var.setText(str(unpack_data[22]))
        self.labelA0_RoomTemp_var.setText(str(round(unpack_data[20], 2)))
        self.labelA1_Humid_var.setText(str(round(unpack_data[21], 2)))
        if unpack_data[38] == 1:
            self.labelD1_lamp_var.setText("HIGH") 
        else:
            self.labelD1_lamp_var.setText("LOW")
        if unpack_data[39] == 1:
            self.labelD2_door_var.setText("HIGH")
        else:
            self.labelD2_door_var.setText("LOW")

    # digital sensor control buttoon 
    def do_control(self) :
        
        # packet 
        STX = 0x0203
        CMD = 0x21
        dummy = 0xff
        mode = 0x00
        result = 0x00
        CRC = 0xffff
        len = 0x00
        # pack packet and send packet 
        value = (STX, CMD, dummy, mode, result, CRC, len, self.d_sensor_no, self.d_sensor_var)
        fmt = '>H B B B B H B B B'.format()
        packer = struct.Struct(fmt)
        cmd = packer.pack(*value)
        self.client_socket.send(cmd) 
        # receive data 
        data = self.client_socket.recv(1024)
        fmt = '>H B B B B H B'.format()
        unpack_data = struct.unpack(fmt, data)
        print(unpack_data)
        

    # system set button 
    def system_set(self):
        STX = 0x0203
        CMD = 0x13
        dummy = 0xff
        mode = 0x00
        result = 0x00
        CRC = 0xffff
        len = 0x00

        value = (STX, CMD, dummy, mode, result, CRC, len, self.ProjectID, self.ProjectName, self.CageID, self.autoInterval,  self.distCalcRate, 
                self.startLab_y, self.startLab_mo, self.startLab_d, self.startLab_h, self.startLab_mi, self.startLab_s, \
                self.stopLab_y, self.stopLab_mo, self.stopLab_d, self.stopLab_h, self.stopLab_mi, self.stopLab_s)
                
        fmt = '>H B B B B H B H 40p H B f H B B B B B H B B B B B'.format()
        packer = struct.Struct(fmt)
        cmd = packer.pack(*value)
        self.client_socket.send(cmd) 
        # receive data 
        data = self.client_socket.recv(1024)
        fmt = '>H B B B B H B'.format()
        unpack_data = struct.unpack(fmt, data)
        print(unpack_data)

     # packet
    def ask_system(self):
        STX = 0x0203
        CMD = 0x14
        dummy = 0xff
        mode = 0x00
        result = 0x00
        CRC = 0xffff
        len = 0x00
        # pack packet and send packet
        value = (STX, CMD, dummy, mode, result, CRC, len)
        fmt = '>H B B B B H B'.format()
        packer = struct.Struct(fmt)
        cmd = packer.pack(*value)
        self.client_socket.send(cmd) 
        # receive data 
        data = self.client_socket.recv(1024)
        fmt = '>H B B B B H B H 40p H 4s 4s 4s B 10p 10p 4s 4s 4s 15p H B B B B B B f H B B B B B H B B B B B 10p 10p'.format()
        unpack_data = struct.unpack(fmt, data)
        print(unpack_data[7])
        print(unpack_data[8])
        print(unpack_data[9])
        print(unpack_data[10])
        print(unpack_data[11])
        print(unpack_data[12])
        self.label_prj_name_var.setText(unpack_data[8].decode())
        self.label_mcu_ip_var.setText(socket.inet_ntoa(unpack_data[10]))
        self.label_mcu_subnet_var.setText(socket.inet_ntoa(unpack_data[11]))
        self.label_mcu_gateway_var.setText(socket.inet_ntoa(unpack_data[12]))
        self.label_wifi_ip_var.setText(socket.inet_ntoa(unpack_data[16]))
        self.label_wifi_subnet_var.setText(socket.inet_ntoa(unpack_data[17]))
        self.label_wifi_gateway_var.setText(socket.inet_ntoa(unpack_data[18]))
        self.label_mcu_time_var.setText(str(unpack_data[20])+str(unpack_data[21])+str(unpack_data[22])+str(unpack_data[23])+str(unpack_data[24])+str(unpack_data[25]))
        self.label_start_lab_var.setText(str(unpack_data[28])+str(unpack_data[29])+str(unpack_data[30])+str(unpack_data[31])+str(unpack_data[32])+str(unpack_data[33]))
        self.label_stop_lab_var.setText(str(unpack_data[34])+str(unpack_data[35])+str(unpack_data[36])+str(unpack_data[37])+str(unpack_data[38])+str(unpack_data[39]))


if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()