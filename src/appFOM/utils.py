""" Contains general methods used by the application
"""
## Lisa tools
import lisaconstants

##
import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline as spline

# pylint: disable=unused-variable

def fast_response(freq, arm_length=2.5e9, tdi2=False):
    """Sky averaged response of the LISA constellation for TDI X.

    :param array freq: frequency range
    :param float arm_length: arm length in meter
    :param bool tdi2: TDI1.5 or 2nd generation
    :return array R: LISA TDI X response
    """
    lisa_lt = arm_length / lisaconstants.SPEED_OF_LIGHT # pylint: disable=no-member
    x = 2.0 * np.pi * lisa_lt * freq
    r = np.absolute(9
                    / 20
                    / (1 + (3 * x / 4) ** 2)
                    * ((16 * x**2 * np.sin(x) ** 2))
                    )
    if tdi2:
        r *= 4 * np.sin(2 * x) ** 2
    return r / 1.5 / 2



def psd2sh(freq, sx, arm_length=2.5e9, tdi2=False, sky_averaging=False):
    """Return sensitivity curve from noise psd.

    :param array freq: frequency range
    :param array SX: noise PSD
    :param bool tdi2: TDI1.5 or 2nd generation
    :param float arm_length: arm length in meter
    :param bool sky_averaging: apply sky averaging factor
    :return array Sh: sensitivity
    """
    lisa_arm_t = arm_length / lisaconstants.SPEED_OF_LIGHT # pylint: disable=no-member
    if tdi2:
        fctr = (
            8.0
            * np.sin(2.0 * np.pi * freq * lisa_arm_t)
            * np.sin(4.0 * np.pi * freq * lisa_arm_t)
        ) ** 2
    else:
        fctr = (4.0 * np.sin(2.0 * np.pi * freq * lisa_arm_t)) ** 2

    f_star = 2.0 * np.pi * lisa_arm_t * freq
    r = 1.0 / (1.0 + 0.6 * (f_star) ** 2)
    fctr = fctr * (2.0 * np.pi * freq * lisa_arm_t) ** 2 * r
    if sky_averaging:
        fctr *= 3 / 20.0
    sh = spline(freq, sx / fctr)
    return sh


# pylint: disable=undefined-variable
def compute_snr(xyz_, sxx_, sxy_):
    """SNR from TDI xyz_

    :param 3xN array xyz_: signal TDI X,Y,Z
    :param 1xN array sxx_: noise PSD auto term
    :param 1xN array sxy_: noise PSD cross term
    :return float snr: total snr from X,Y,Z combination.
    """
    efact = sxx_ * sxx_ + sxx_ * sxy_ - 2 * sxy_ * sxy_
    efact[efact == 0] = np.inf
    efact = 1 / efact
    exx = (sxx_ + sxy_) * efact
    exy = -sxy_ * efact

    snr = 0
    for k in range(3):
        snr += np.sum(np.real(xyz_[k] * np.conj(xyz_[k]) * exx))
    for k1, k2 in [(0, 1), (0, 2), (1, 2)]:
        snr += np.sum(np.real(xyz_[k1] * np.conj(xyz_[k2]) * exy))
        snr += np.sum(np.real(xyz_[k2] * np.conj(xyz_[k1]) * exy))
    snr *= 4.0 * df
    return np.sqrt(snr)
