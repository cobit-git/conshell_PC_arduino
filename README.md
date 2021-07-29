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








