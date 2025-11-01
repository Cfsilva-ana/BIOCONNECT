#include <WiFi.h>        

const int ecgPin = 34;           // pino ADC do AD620
const float adcRef = 3.3;        // tensão de referência
const int adcRes = 4095;         // resolução do ADC do ESP32

unsigned long lastBeatTime = 0;
bool beatDetected = false;


const float THRESHOLD = 0.2;

const char* ssid     = "BUG_SLAYER";
const char* password = "4ipaipara";

void setup() {
  Serial.begin(115200);
  delay(100);

  Serial.println();
  Serial.println("=== Iniciando ESP32 ===");

  // Conecta ao WiFi
  Serial.print("Conectando em ");
  Serial.print(ssid);
  Serial.print(" ... ");
  WiFi.begin(ssid, password);

  unsigned long startAttemptTime = millis();
  
  while (WiFi.status() != WL_CONNECTED && millis() - startAttemptTime < 10000) {
    Serial.print(".");
    delay(500);
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println();
    Serial.println("WiFi conectado!");
    Serial.print("IP local: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println();
    Serial.println("Falha ao conectar WiFi (timeout). Continuando sem rede...");
  }

  Serial.println("Iniciando leitura do ECG...");
}


void loop() {
  int adcValue = analogRead(ecgPin);
  float voltage = adcValue * (adcRef / adcRes);


  if (voltage > THRESHOLD && !beatDetected) {
    unsigned long currentTime = millis();

    if (lastBeatTime != 0) {
      float bpm = 60000.0 / (currentTime - lastBeatTime);  // calcula BPM
      lastBeatTime = currentTime;

      Serial.print("BPM: ");
      Serial.println(bpm, 1);  // 1 casa decimal

      // Alertas
      if (bpm >= 150) {
        Serial.println("⚠️ Infarto eminente!!! Chamando ambulancia.");
      } else if (bpm < 50) {
        Serial.println("⚠️ Parada cardiaca, ambulancia a caminho.");
      }

    } else {
      lastBeatTime = currentTime;  // primeiro batimento
    }

    beatDetected = true;
  }

  if (voltage < THRESHOLD) {
    beatDetected = false;
  }


  delay(2); 
}
