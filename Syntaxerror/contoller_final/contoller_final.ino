#define button_j 7
#define button_1 6
#define button_2 5
#define button_3 4
#define led_pin LED_BUILTIN


int button1_state,button2_state,button3_state,button4_state, x_value, y_value, j_b_value;
 
void setup() {
  Serial.begin(9600);
  pinMode(button_j, INPUT_PULLUP);
//  pinMode(led_pin, OUTPUT);
  pinMode(button_1, INPUT_PULLUP);
  pinMode(button_2, INPUT_PULLUP);

  pinMode(button_3, INPUT_PULLUP);



}

void writeData(int x, int y, int but_j, int b1, int b2, int b3){
  Serial.print(x);
  Serial.print(" || ");
  Serial.print(y);
  Serial.print(" || ");
  Serial.print(but_j);
  Serial.print(" || ");
  Serial.print(b1);
  Serial.print(" || ");
  Serial.print(b2);
  Serial.print(" || ");
  Serial.print(b3);
  Serial.print("\n");
  Serial.flush();
  
}


void loop() {
  x_value = analogRead(A0);
  y_value = analogRead(A1);
  j_b_value = digitalRead(button_j);
  button1_state = digitalRead(button_1);
  button2_state = digitalRead(button_2);
  button3_state = digitalRead(button_3);

  writeData(x_value, y_value, j_b_value, button1_state, button2_state, button3_state);

}
