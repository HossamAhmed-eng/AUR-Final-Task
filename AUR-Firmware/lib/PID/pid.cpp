#include "pid.h"
#include "Arduino.h"
#include "float.h"
#include <math.h>

#define clamp(v, l, h) (min(max(v, l), h))

PID::PID(float kp, float ki, float kd, float max_output)
    : kp(kp), ki(ki), kd(kd), max_output(max_output),
      accumulated_error(0), prev_error(0), prev_time(0) {}

double PID::get_output(double target, double current) {
    const unsigned long now = micros();
    const double dt = (now - prev_time) / 1000000.0;
    if (dt <= DBL_EPSILON) return 0;

    const double err = target - current;
    accumulated_error += err * dt;
    accumulated_error = clamp(accumulated_error, -max_output, max_output);

    const double p = kp * err;
    const double i = ki * accumulated_error;
    const double d = kd * (err - prev_error) / dt;

    double output = p + i + d;
    output = clamp(output, - max_output, max_output);

    prev_error = err;
    prev_time = now;
    return output;
}
