#include "pid.h"
#include <float.h>
#include <algorithm>

static inline double clampd(double v, double l, double h)
{
    return std::min(std::max(v, l), h);
}

PID::PID(float kp, float ki, float kd, float max_output)
    : kp(kp), ki(ki), kd(kd),
      max_output(max_output),
      prev_error(0), accumulated_error(0), prev_time(0) {}

double PID::get_output(double target, double current)
{
    unsigned long now = micros();
    double dt = (now - prev_time) / 1e6;
    if (dt <= DBL_EPSILON)
        return 0;

    double err = target - current;
    accumulated_error += err * dt;
    accumulated_error = clampd(accumulated_error, -max_output, max_output);

    double p = kp * err;
    double i = ki * accumulated_error;
    double d = kd * (err - prev_error) / dt;

    double output = p + i + d;
    output = clampd(output, -max_output, max_output);

    prev_error = err;
    prev_time = now;
    return output;
}
