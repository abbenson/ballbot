import math


def get_velocities(pitch_vel_l, pitch_vel_r, roll_vel_l, roll_vel_r, pitch, roll):
    """
    Returns an estimated bot velocity
    :param pitch_vel_l: Left pitch motor velocity
    :param pitch_vel_r: Right pitch motor velocity
    :param roll_vel_l: Left roll motor velocity
    :param roll_vel_r: Right roll motor velocity
    :param pitch: Bot pitch angle
    :param roll: Bot roll angle
    :return: Velocities in the x and y axis
    """
    v_x = .5 * (pitch_vel_l + pitch_vel_r)
    v_y = .5 * (roll_vel_l + roll_vel_r)
    pitch = math.radians(pitch)
    roll = math.radians(roll)
    v_x *= math.cos(pitch)
    v_y *= math.cos(roll)
    return v_x, v_y
