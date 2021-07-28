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
