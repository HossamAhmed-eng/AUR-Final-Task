#ifndef PID_H
#define PID_H
class PID {
   float kp, ki, kd;
   float prev_error; // derivative 
   unsigned long long prev_time;  //dt
   float max_output;
   float accumulated_error; // integral
public:
      
 PID(float kp, float ki, float kd, float max_output);
    double get_output(double target, double current);

    };
#endif 