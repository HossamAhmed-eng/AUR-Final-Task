#pragma once
#include <Arduino.h>

class PID
{
public:
   PID(float kp, float ki, float kd, float max_output);
   double get_output(double target, double current);

private:
   float kp, ki, kd;
   float max_output;
   float prev_error;
   float accumulated_error;
   unsigned long prev_time;
};
