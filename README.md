# 콘쉘 스마트 케이지 프로젝트
## 콘쉘 스마트 케이지 전체 구성도 
## 아두이노 센서 구성도 
![image](https://user-images.githubusercontent.com/76054530/127325299-34138f2a-547c-4cd0-baf4-91cf6a1d8066.png)

아두이노 보드에는 HX711 기반의 로드셀 센서, DHT22 기반의 온도/습도 센서, ON/OFF 스위치, LED 모듈이 연결되어 있습니다. 

#### 온도/습도 모듈 DHT22 모듈: GPIO 11
#### 로드셀(저울) 모듈 HX711 모듈: DOUT ->3, SCK -> 2
#### ON/OFF 스위치: GPIO 13
#### LED 모듈: GPIO 7


## 센서 컨트롤용 아두이노 코드 
### 라이브러리 설치 
위 센서들을 동작시키려면 다음 라이브러리를 설치합니다. 
온도/습도 센서인 DHT22용 라이브러리는 "DHT Sensor Library" 입니다. 이 라이브러리를 설치하고 다음 헤더파일을 포함합니다. 
```C
#include <DHT.h>
#include <DHT_U.h>
```
라이브러리 참고 URL은 다음을 참고해 주십시오.
[DHT22 아두이노 라이브러리](https://github.com/adafruit/DHT-sensor-library)

DHT22 센서를 사용하기 위해서는 다음 라이브러리를 추가로 설치해야 합니다. 이 라이브러리를 설치하고 다음 헤더파일을 포함합니다. 
```C
#include <Adafruit_Sensor.h>
```
라이브러리 참고 URL은 다음을 참고해 주십시오.
[Adafruit Unified Sendor 라이브러리](https://github.com/adafruit/Adafruit_Sensor)

로드셀 센서 HX711 센서용 라이브러리는 "HX711 Arduino Library" 입니다. 이 라이브러리를 설치하고 다음 헤더파일을 포함합니다. 
```C
#include "HX711.h"
```
라이브러리 참고 URL은 다음을 참고해 주십시오.
[HX711 아두이노 라이브러리](https://github.com/bogde/HX711)

## 아두이노 라즈베리파이 프로토콜 
### 아두이노 -> 라즈베리파이 센서 데이터 프로토콜 
아두이노가 수집한 센서 데이터는 시리얼 통신을 통해서 라즈베리파이로 전달이 됩니다. 두 기기간의 통신 프로토콜은 다음과 같습니다. 
<pre><code>
protocol: a+"roadcell value"+b+"temperature value"+c+"humidity value"+d+"switch on/off"+e
</code></pre>

### 라즈베리파이 -> 아두이노 IO 데이터 프로토콜
PC클라이언트에서 아두이노 IO를 on/off 하기 위해서 커맨드를 전달 할 수 있습니다. 역시 통신은 시리얼을 통해서 이루어 집니다. 
라즈베리파이가 PC클라이언트의 데이터를 받는 프로토콜은 다음과 같습니다. 
<pre><code>
Raspberry send "a1" or "a0"
a0 -> turn off LED
a1 -> turn on LED 
</code></pre>


## 스마트 케이지 서버 통신용 클라이언트 파이썬 코드 
### PC 클라이언트
PC 클라이언트는 라즈베리파이에서 동작하는 스마트 케이지 서버와 통신하고, 스마트 케이지 서버가 전달하는 데이터를 PC에 UI 화면으로 보여주는 파이썬 코드입니다. 
이 PC 쿨라이언트는 콘쉘의 결국에는 모니터링 프로그램으로 대체 되어야 합니다. 이 파이썬 코드는 스마트 케이지 서버가 제대로 동작하는지 체크하기 위해 임시로 개발한 tool 입니다. 
PC클라이언트 프로그램을 실행할 PC에 파이썬 3.x 버전이 설치되어 있어야 합니다. 

### 라즈베리파이 스마트 케이지 서버와 PC 클라이언트와 통신
라즈베리파이에서 동작하는 스마트 케이지 서버와 PC클라이언트는 소켓 통신을 통해서 통신을 합니다. 구체적인 통신의 개념도는 다음과 같습니다.    
![image](https://user-images.githubusercontent.com/76054530/127469496-7e81818b-f5d0-4b36-8c67-9d7e90da7bb5.png)

### 파이썬 라이브러리 임포트 
PC클라이언트 파이썬 코드를 실행하기 위해서 다음과 같은 파이썬 라이브러리를 임포트 합니다. 
```python
import sys
import socket 
import struct
from PyQt5.QtWidgets import *
from PyQt5 import uic
```

이 중에서 PyQt5 라이브러리는 별도로 설치를 해 주어야 합니다. 다음과 같이 설치를 합니다. 
<pre><code>
$pip install pyqt5
</code></pre>

### PC클라이언트 프로그램 실행 화면 
PC클라이언트 프로그램은 다음과 같이 실행하면 됩니다. 
<pre><code>
$python conshell_monitor_pyqt.py
</code></pre>

프로그램이 실행되면 다음과 같은 화면이 디스플레이 됩니다. 
![image](https://user-images.githubusercontent.com/76054530/127475491-ed88ff1d-66b0-4e6e-87fa-aa9739d7b90a.png)


### PC클라이언트 프로그램 파이썬 코드 
#### UI 파일 로드 
PC클라이언트 프로그램은 PyQt5를 이용해서 UI 화면을 구성합니다. 그래서 UI 파일이 필요합니다. UI 파일은 "conshell_ui.ui" 입니다. 깃허브에 PC클라이언트 프로그램과 같이 다운로드 됩니다. 
UI 파일의 로드는 다음과 같이 합니다. 
```python
form_class = uic.loadUiType("conshell_ui.ui")[0]
```
#### 메인 윈도 클래스 
PC클라이언트의 UI를 그려주는 클래스는 다음과 같습니다. 이 클래스에서 UI를 그려주고, 소켓 통신을 열고, 관리 합니다. 
```python
class WindowClass(QMainWindow, form_class) :
```

#### 소켓 통신용 IP 어드레스 및 포트번호 설정 
라즈베리파이에서 동작하는 스마트 케이즈 서버에 접속하려면 스마트 서버의 IP, 즉 라즈베리파이의 IP를 알아야 합니다. 라즈베리파이 IP를 다음 코드와 같이 셋팅합니다.    
포트 번호는 9998을 사용했습니다.    
```python 
self.host = '172.31.99.2'
self.port = 9998
```

#### 소켓 통신 연결하기 
소켓 통신은 다음과 같은 코드로 연결을 합니다. 
```python
self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
self.client_socket.connect((self.host, self.port))
```

#### 버튼 클릭 셋팅 
PyQt5 버튼 기능을 셋팅합니다. 콘쉘 프로토콜 중 4개의 프로토콜을 구현했습니다. 다음의 코드는 각각의 버튼에 프로토콜을 실행하는 함수를 맵핑하는 코드입니다. 
```python
# conshell protocol 0x51, cage status, make button and resiter handler function 
self.askStatus.clicked.connect(self.ask_Status)
# conshell protocol 0x25, sensor control, make button and resiter handler function
self.doControl.clicked.connect(self.do_control)
# conshell protocol 0x13, system setting, make button and resiter handler function
self.systemSet.clicked.connect(self.system_set)
# conshell protocol 0x24, system status, make button and resiter handler function 
self.askSystem.clicked.connect(self.ask_system)
```

#### 콘쉘 프로토콜 0x13 시스템 셋팅 에디트 텍스트 박스 코드 
콘쉘 프로토콜 0x13 시스템 셋팅 에디트 테스트 박스는 다음코드로 구현되어 있습니다.    
각각의 에디트텍스트에 데이터를 입력하고 "시스템셋팅(0x13)" 버튼을 클릭하면 데이터가 스마트케이지 서버로 전송이 됩니다.    
```python
# conshell protocol 0x13 system setting - edit text box
self.edt_set_project_id.textChanged.connect(self.set_project_id)
self.edt_set_project_name.textChanged.connect(self.set_project_name)
self.edt_set_cage_id.textChanged.connect(self.set_cage_id)
self.edt_set_start_time.textChanged.connect(self.set_start_time)
self.edt_set_stop_time.textChanged.connect(self.set_stop_time)
self.edt_set_calc_rate.textChanged.connect(self.set_calc_rate)
```

#### 콘쉘 프로토콜 0x25 디지털 센서 제어 에디트 텍스트 박스 코드 
콘쉘 프로토콜 0x25 디지털 센서 제어 에디트 테스트 박스는 다음코드로 구현되어 있습니다. 
```python
# conshell protocol 0x25 sensor control - edit text box 
self.edt_d_sensor_no.textChanged.connect(self.set_d_sensor_no)
self.edt_d_sensor_var.textChanged.connect(self.set_d_sensor_var)
```

#### ask_Status() 함수 
이 함수는 콘쉘 프로토콜 0x51을 구현한 함수 입니다. 다음과 같이 요청 패킷을 전송합니다. 
```python
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
```
이 요청을 받은 스마트 케이지 서버는 콘쉘의 프로토콜 0x51에 따라 케이지 상태 정보를 보냅니다. 이 정보를 다음 코드로 받습니다. 
```python
 # receive data 
 data = self.client_socket.recv(1024)
```
그리고 다음 코드로 파싱을 해서 데이터를 얻습니다. 
```python 
# parsing data
fmt = '>H B B B B H B H H B I f H H I H H I H H f f f I I I I I I I I I I I I I I B B B B B B B B B B B B B B B B B'.format()
unpack_data = struct.unpack(fmt, data)
print(unpack_data)
```
그 다음에는 데이터를 UI 화면에 채워 넣습니다. 
```python
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
````
#### do_control() 함수 
이 함수는 콘쉡 프로토콜 0x25 디지털 센서 제어를 구현한 함수 입니다. 다음과 같이 제어하고 싶은 센서번호와 값을 입력하고 요청 패킷을 보냅니다. 
```python
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
 ```
 이 요청을 받은 스마트 케이지 서버는 콘쉘의 프로토콜 0x51에 따라 디지털 센서를 셋팅하고 회신 패킷을 보냅니다. 이 정보를 다음 코드로 받습니다. 
```python
 # receive data 
 data = self.client_socket.recv(1024)
 ```
 
 회신된 데이터를 파싱합니다. 
 ```python
 # parsing data 
 fmt = '>H B B B B H B'.format()
 unpack_data = struct.unpack(fmt, data)
 print(unpack_data)
 ```
#### system_set() 함수 
이 함수는 콘쉘 프로토콜 0x13 시스템 셋팅을 구현함 함수 입니다. 미리 UI를 통해서 시스템 셋팅할 값을 정합니다.    
그 다음에 다음과 같은 코드로 시스템 셋팅 요청을 스마트 케이지 서버에 보냅니다. 
```python
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
```

이 요청을 받은 스마트 케이지 서버는 보내진 시스템 정보를 셋팅하고 회신 패킷을 보냅니다. 이 패킷은 다음과 같이 받습니다. 
```python
# receive data 
data = self.client_socket.recv(1024)
```
 회신된 데이터를 파싱합니다. 
```python
# parsing data 
fmt = '>H B B B B H B'.format()
unpack_data = struct.unpack(fmt, data)
print(unpack_data)
```

#### ask_system() 함수 
이 함수는 콘쉘 프로토콜 0x14 시스템 정보 요청을 구현한 함수 입니다. 다음과 같이 요청 패킷을 보냅니다. 
```python
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
```
이 요청을 받은 스마트 케이지 서버는 콘쉘의 프로토콜 0x14에 따라 시스템 상태 정보를 보냅니다. 이 정보를 다음 코드로 받습니다.
```python
# receive data 
data = self.client_socket.recv(1024)
```
받은 정보는 다음 코드로 파싱하고, UI의 각 해당 위치를 업데이트 합니다. 
```python
# parsing data 
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
```
#### PC클라이언트 메인 코드 
PC클라이언트의 메인 코드는 다음과 같다. 
```python
#QApplication : 프로그램을 실행시켜주는 클래스
app = QApplication(sys.argv) 

#WindowClass의 인스턴스 생성
myWindow = WindowClass() 

#프로그램 화면을 보여주는 코드
myWindow.show()

#프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
app.exec_()
```
