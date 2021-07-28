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

DHT22 센서를 사용하기 위해서는 다음 라이브러리를 추가로 설치해야 합니다. 이 라이브러리를 설치하고 다음 헤더파일을 포함합니다. 
```C
#include <Adafruit_Sensor.h>
```

로드셀 센서 HX711 센서용 라이브러리는 "HX711 Arduino Library" 입니다. 이 라이브러리를 설치하고 다음 헤더파일을 포함합니다. 
```C
#include "HX711.h"
```

## 스마트 케이지 서버 통신용 클라이언트 파이썬 코드 
