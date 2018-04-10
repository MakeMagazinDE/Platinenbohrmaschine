#include <AccelStepper.h>

#define enaPin 2        // Schrittmotor Enable für Schrittmotorsteuerung
#define pwmPin 3        // PWM-Pin für Spindeldrehzahl
#define dirPin 4        // Schrittmotor Richtungspin für Schrittmotorsteuerung
#define stepPin 5       // Schrittmotor Schrittspin für Schrittmotorsteuerung
#define TasterPin 6     // Tasterpin fuer Werkzeuglaenge
#define SensorPin 7     // Sensorpin fuer Nullpunkt
#define hipwr_Pin 8     // Optokoppler UB36
#define pwron_Pin 9     // Einschaltrelais fuer 5V RPi
#define shutdwn_Pin 10  // Raspberry GPIO shutdwn => Startet am RPi das Shutdown-Script
#define chkdwn_Pin 11   // Raspberry GPIO dwn chk => Prueft ob RPi heruntergefahren ist
#define isdwn_Pin 12    // LED zur Anzeige, dass RPi heruntergefahren ist

AccelStepper stepper(1, stepPin, dirPin);   // Schrittmotor initialisieren Mode 1

const int shudwn_zeit = 30; // Schutdown-Zeit fuer RPi [s]
const int einschaltverz = 5; // Einschaltverzoegerung fuer RPi [s]

int bg;   // Bohrgeschwindigkeit
int ba;   // Bohrbeschleunigung
int wp;   // Werkzeugwechselposition
int bt;   // Bohrtiefe
int wl;   // Werkzeuglänge
int hp;   // Homeposition
int su;   // Schritte je Umdrehung
int ss;   // Hub in mm je Umdrehung
int pw;   // Drehzahl 0 .. 100%


int state = 0;      // Buffer fuer UB36 Kontrolle
int laststate = 0;  // Buffer fuer UB36 Kontrolle
int bohrtiefe;      // Bohrtiefe in Schritten
int wkzpos;         // Werkzeugwechselposition in Schritten
int homepos;        // Homeposition in Schritten
int nullpos;        // Referenzposition

void setup()
{
  Serial.begin(9600);                 // Konfiguration der seriellen Schnittstelle

  pinMode(TasterPin, INPUT);          // Werkzeuglängensensor
  digitalWrite(TasterPin, HIGH);      // Pull-up Widerstand fuer Taster
  pinMode(SensorPin, INPUT);          // Referenzsensor fuer Null-Position (unteres Ende)
  pinMode(hipwr_Pin, INPUT);          // Pin fuer Pruefung von UB36
  pinMode(pwron_Pin, OUTPUT);         // Pin fuer Relais zum Einschlaten des RPi
  pinMode(shutdwn_Pin, OUTPUT);       // Pin zum Starten des Shutdown des RPi (ueber GPIO)
  pinMode(chkdwn_Pin, INPUT);         // Pin zum Pruefen ob RPi heruntergefahren ist
  pinMode(isdwn_Pin, OUTPUT);         // Pin fuer LED, die anzeigt, dass RPi herunter gefahren ist

  analogWrite(pwmPin, 0);             // Spindel anhalten
  digitalWrite(shutdwn_Pin, HIGH);    // Shutdown Pin auf HIGH => RPi GPIO18 = HIGH
  digitalWrite(pwron_Pin, HIGH);      // Raspberry einschalten => Relais fuer Spannungsversorgung RPi ein
  laststate = digitalRead(hipwr_Pin); // Zustand von UB36 initialisieren

  
  Config();                           // Einlesen des Configfiles vom RPI in den Arduino
  CheckConfig();                      // Ausgabe der Config am RPi im Statusfenster

  stepper.setMaxSpeed(1000);          // maximale Geschwindigkeit - Schritte pro Sekunde
  stepper.setSpeed(bg);               // Geschwindigkeit - Schritte pro Sekunde
  stepper.setAcceleration(ba);        // Beschleunigung - Schritte pro Sekunde im Quatrad

  StepperRef();                       // Schrittmotor in Nullposition
}

//============================================



void Config() {                     // Einlesen der Configuraion vom RPi
  char CommandBuffer[200];          // Zeichenbuffer
  char c;                           // serielles Zeichen
  int i = 0;                        // Laufvariable
  int TrennerPos;                   // Zeichenposition des Trennzeichens '\n'
  String CommandString;             // der gesamte Config Inhalt
  String Command;                   // der einzelne Befehl (Komando und Wert)
  String SCmd;                      // der geteilte Befehl (Komando)
  String SVal;                      // der geteilte Befehl (Wert)

  delay(1000);                      // eine Sekunde warten
  Serial.print("Reading Config\n"); // Ausgabe auf RPi

  memset(CommandBuffer, 0, sizeof(CommandBuffer));  // Puffer mit Nullbytes fuellen und dadurch loeschen
  do {                                              // Configfile vom RPi empfangen
    Serial.print(".");                              // Lebenszeichen
    if (Serial.available()) {
      delay(100);
      while (Serial.available()) {
        c = Serial.read();
        CommandBuffer[i] = c;
        i++;}}

    CommandString = String(CommandBuffer);          // Config-Inhalte in String umwandeln

    do {
      TrennerPos = CommandString.indexOf('\n');     // Trennerposition suchen
      if (TrennerPos != -1) {
        Command = CommandString.substring(0, TrennerPos); // einzelnen Befehl suchen
        SCmd = Command.substring(0, 3);                   // Befehl aufteilen
        SVal = Command.substring(3);  
        CommandString = CommandString.substring(TrennerPos + 1, CommandString.length());  // naechsten Befehl

        if (SCmd.equals("bg="))                     // Befehl auswerten
          bg = SVal.toInt();                        // Wert in int wandeln und in Variablen schreiben
        else if (SCmd.equals("ba="))
          ba = SVal.toInt();
        else if (SCmd.equals("wp="))
          wp = SVal.toInt();
        else if (SCmd.equals("bt="))
          bt = SVal.toInt();
        else if (SCmd.equals("wl="))
          wl = SVal.toInt();
        else if (SCmd.equals("hp="))
          hp = SVal.toInt();
        else if (SCmd.equals("su="))
          su = SVal.toInt();
        else if (SCmd.equals("ss="))
          ss = SVal.toInt();
        else if (SCmd.equals("pw="))
          pw = SVal.toInt();}}
    while (TrennerPos >= 0);
    delay(500);}
  while (pw < 1);                                   // Letzter Befehl wenn pw einen Inhalt hat

  bohrtiefe = bt * su / ss;                         // Bohrtiefe in Schritte umrechnen
  wkzpos = -1 * wp * su / ss;                       // Werkzeugposition in Schritte umrechnen
  homepos = -1 * hp * su / ss;                      // Home-Position in Schritte umrechnen
  
  Serial.println("Config done\n");}                 // Bestaetigung an RPi

void CheckConfig() {                                // Config am RPi ausgeben
  Serial.println("Config Check\n");
  Serial.print("bg: ");
  Serial.println(bg);
  Serial.print("ba: ");
  Serial.println(ba);
  Serial.print("wp: ");
  Serial.println(wp);
  Serial.print("bt: ");
  Serial.println(bt);
  Serial.print("wl: ");
  Serial.println(wl);
  Serial.print("hp: ");
  Serial.println(hp);
  Serial.print("su: ");
  Serial.println(su);
  Serial.print("ss: ");
  Serial.println(ss);
  Serial.print("pw: ");
  Serial.println(pw);
}

void rasp_dwn(){                          // Ueberpreufen der UB36 und RPi ein-/ ausschalten incl. sicherer Shutdown

  state = digitalRead(hipwr_Pin);         // UB36 pruefen
  
  
  if (laststate == HIGH && state == LOW)  // => 36V-Netzteil wurde eingeschaltet
    {
    digitalWrite(shutdwn_Pin, HIGH);      // => RPi GPIO18 HIGH 
    delay(1000);
    digitalWrite(pwron_Pin, HIGH);        // => Relais fuer RPi Spannung eingeschaltet lassen 
    Serial.print("RPi Spannung da\n");    // => ser. Meldung an RPi, dass ausgeschaltet wird    
    delay(1000*einschaltverz);            // => Einschaltverzoegerung warten (RPi startet)
    Config();                             // nach dem EInschalten Config Daten einlesen
    CheckConfig();                        // eingelesene Config an RPi anzeigen
    }
  else if (laststate == LOW && state == HIGH) // 36V-Netzteil wurde ausgeschaltet  
    {
    Serial.print("os: SHUTDOWN -h now\n"); // => ser. Meldung an RPi, dass heruntergefahren wird
    digitalWrite(shutdwn_Pin, LOW);       // => RPi GPIO18 LOW => RPi fuerht shutdown -h now aus
    delay(1000*shudwn_zeit);              // => Shutdownzeit warten (RPi sicher herunter fahren)
    digitalWrite(shutdwn_Pin, HIGH);       // => Damit beim Neustart nicht gleich wieder schutdown passiert
    Serial.print("RPi Spannung weg\n");   // => ser. Meldung an RPi, dass ausgeschaltet wird
    digitalWrite(pwron_Pin, LOW);         // Relais fuer Spannungsversorgung RPi ausscahlten
    }
    else;

    laststate = state;                    // state in laststate sichern
    
  if (digitalRead(chkdwn_Pin) == LOW)     // => Rueckmeldung vom RPi, Shudwon fertig ueber GPIO27
    digitalWrite(isdwn_Pin, HIGH);        // => LED "Shutdown feritg" an
  else
    digitalWrite(isdwn_Pin, LOW);         // => LED "Shutdown feritg" aus
}

void StepperRef()                         // Z-Achse in Null-Position (Referenz) fahren
{
  while (digitalRead(SensorPin) == LOW)   // Positionssensor lesen
  {
    stepper.move(100);                    // Schrittmotor nach unten fahren bis Sensor LOW
    stepper.run();
  }
  nullpos = stepper.currentPosition();    // Refernezposition sichern
  Serial.print("p=");                     // aktuelle Position an RPi
  Serial.println(nullpos);                // aktuelle Position an RPi

}

void StepperHome()                        // Z-Achse zur Homeposition (Bohrerspitze unter Bohrtisch)
{
  stepper.runToNewPosition(homepos);      
  Serial.print("p=");
  Serial.println(stepper.currentPosition());  // aktuelle Position an RPi
}

void StepperWkz()                         // Z-Achse zur Werkzeugwechselposition
{
  stepper.runToNewPosition(wkzpos);
  Serial.print("p=");
  Serial.println(stepper.currentPosition());  // aktuelle Position an RPi
}

void Bohren()
{
  StepperHome();                                    // Z-Achse zur Homeposition
  analogWrite(pwmPin, pw);                          // Fraeser mit pw-Drehzahl einschalten
  delay(1000);                                      // warten bis Fraeser auf Drehzahl
  stepper.runToNewPosition(homepos - bohrtiefe);    // Bohren auf Bohrtiefe
  stepper.runToNewPosition(homepos);                // zurueck zur Homeposition
  analogWrite(pwmPin, 0);                           // Fraser ausschalten
  Serial.print("p=");
  Serial.println(stepper.currentPosition());        // aktuelle Position an RPi
}

void Werkzeuglaenge()                               // Werkzeuglaenge messen
{
  while (digitalRead(TasterPin) == HIGH)            // solange Wwerkzeuglaengensensor nicht betaetigt
  {
    stepper.move(-100);                             // Schrittmotor nach oben fahren
    stepper.run();
  }
  homepos = stepper.currentPosition();              // wenn Taster gedrueckt diese Position als neue Homeposition sichern
  Serial.print("p=");
  Serial.println(homepos);                          // aktuelle Position an RPi
  StepperHome();                                    // eigentlich ueberfluessig, da sich die Z-Achse bereits hier befindet
}

void Pwm(int n)                                     // Drehzahlstuerung fuer Fraeser
{
  pw = n;
  Serial.print("pwm: ");
  Serial.println(pw);
}

void CheckSerial()                                  // Auf Steuerungsbefehle von RPi warten
{
  if (Serial.available())
  {
    byte nr = Serial.read();
    switch (nr)
    {
      case 0:                                       // Z-Achse in Homeposition
        StepperHome();      
        break;
      case 1:                                       // Z-Achse Referenzfahrt durchfuehren
        StepperRef();
        break;
      case 2:                                       // Z-Achse in Werkzeugwechselposition
        StepperWkz();
        break;
      case 3:                                       // Bohren
        Bohren();
        break;
      case 4:                                       // Werkzeuglaenge messen
        Werkzeuglaenge();
        break;
      case 5:                                       // Drehzahl 0%
        Pwm(0);
        break;
      case 6:                                       // Drehzahl 25%
        Pwm(60);
        break;
      case 7:                                       // Drehzahl 50%
        Pwm(120);
        break;
      case 8:                                       // Drehzahl 75%
        Pwm(180);
        break;
      case 9:                                       // Drehzahl 100%
        Pwm(240);
        break;
    }
  }
}

//============================================

void loop()
{
  rasp_dwn();                                       // UB36 pruefen - ob neu ein- oder ausgeschaltet
  for (int i=0; i < 100;  i++)
    CheckSerial();                                  // auf Steuerbefehle vom RPi testen
}
