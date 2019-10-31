#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: FM receiver
# Generated: Thu Oct 31 08:51:38 2019
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import osmosdr
import time
import wx


class RECEPTOR_FM(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="FM receiver")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 2e6
        self.down_rate = down_rate = 150e3
        self.VOLUMEN = VOLUMEN = 70
        self.SINTONIZADOR = SINTONIZADOR = 90.1e6
        self.GANANCIA = GANANCIA = 50

        ##################################################
        # Blocks
        ##################################################
        _VOLUMEN_sizer = wx.BoxSizer(wx.VERTICAL)
        self._VOLUMEN_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_VOLUMEN_sizer,
        	value=self.VOLUMEN,
        	callback=self.set_VOLUMEN,
        	label='Ajuste de sonido',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._VOLUMEN_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_VOLUMEN_sizer,
        	value=self.VOLUMEN,
        	callback=self.set_VOLUMEN,
        	minimum=0,
        	maximum=100,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_VOLUMEN_sizer, 1, 5, 1, 8)
        _SINTONIZADOR_sizer = wx.BoxSizer(wx.VERTICAL)
        self._SINTONIZADOR_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_SINTONIZADOR_sizer,
        	value=self.SINTONIZADOR,
        	callback=self.set_SINTONIZADOR,
        	label='Sintonizador',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._SINTONIZADOR_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_SINTONIZADOR_sizer,
        	value=self.SINTONIZADOR,
        	callback=self.set_SINTONIZADOR,
        	minimum=10e6,
        	maximum=142e6,
        	num_steps=10,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_SINTONIZADOR_sizer)
        _GANANCIA_sizer = wx.BoxSizer(wx.VERTICAL)
        self._GANANCIA_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_GANANCIA_sizer,
        	value=self.GANANCIA,
        	callback=self.set_GANANCIA,
        	label='Ganancia',
        	converter=forms.int_converter(),
        	proportion=0,
        )
        self._GANANCIA_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_GANANCIA_sizer,
        	value=self.GANANCIA,
        	callback=self.set_GANANCIA,
        	minimum=10,
        	maximum=70,
        	num_steps=12,
        	style=wx.SL_HORIZONTAL,
        	cast=int,
        	proportion=1,
        )
        self.GridAdd(_GANANCIA_sizer, 1, 0, 1, 4)
        self.wxgui_fftsink2_1 = fftsink2.fft_sink_f(
        	self.GetWin(),
        	baseband_freq=0,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=1024,
        	fft_rate=1000,
        	average=False,
        	avg_alpha=None,
        	title='Especto de frecuencias',
        	peak_hold=False,
        )
        self.Add(self.wxgui_fftsink2_1.win)
        self.rtlsdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + '' )
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(SINTONIZADOR, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(0, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0.set_gain(GANANCIA, 0)
        self.rtlsdr_source_0.set_if_gain(20, 0)
        self.rtlsdr_source_0.set_bb_gain(20, 0)
        self.rtlsdr_source_0.set_antenna('', 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)
          
        self.rational_resampler_xxx_1 = filter.rational_resampler_fff(
                interpolation=48,
                decimation=50,
                taps=None,
                fractional_bw=None,
        )
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccf(
                interpolation=1,
                decimation=4,
                taps=None,
                fractional_bw=None,
        )
        self.low_pass_filter_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, samp_rate, 100e3, 1e6, firdes.WIN_HAMMING, 6.76))
        self.blocks_wavfile_sink_0 = blocks.wavfile_sink('C:\\Users\\camil\\Desktop\\PROYECTO DE PRUEBA\\Decodificador\\DemodulacionFM.wav', 1, 20800, 16)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((VOLUMEN/100, ))
        self.audio_sink_0 = audio.sink(48000, '', True)
        self.analog_wfm_rcv_0 = analog.wfm_rcv(
        	quad_rate=500000,
        	audio_decimation=10,
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_wfm_rcv_0, 0), (self.rational_resampler_xxx_1, 0))    
        self.connect((self.analog_wfm_rcv_0, 0), (self.wxgui_fftsink2_1, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.audio_sink_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_wavfile_sink_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.analog_wfm_rcv_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.low_pass_filter_0, 0))    
        self.connect((self.rational_resampler_xxx_1, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.rtlsdr_source_0, 0), (self.rational_resampler_xxx_0, 0))    

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.wxgui_fftsink2_1.set_sample_rate(self.samp_rate)
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 100e3, 1e6, firdes.WIN_HAMMING, 6.76))

    def get_down_rate(self):
        return self.down_rate

    def set_down_rate(self, down_rate):
        self.down_rate = down_rate

    def get_VOLUMEN(self):
        return self.VOLUMEN

    def set_VOLUMEN(self, VOLUMEN):
        self.VOLUMEN = VOLUMEN
        self._VOLUMEN_slider.set_value(self.VOLUMEN)
        self._VOLUMEN_text_box.set_value(self.VOLUMEN)
        self.blocks_multiply_const_vxx_0.set_k((self.VOLUMEN/100, ))

    def get_SINTONIZADOR(self):
        return self.SINTONIZADOR

    def set_SINTONIZADOR(self, SINTONIZADOR):
        self.SINTONIZADOR = SINTONIZADOR
        self._SINTONIZADOR_slider.set_value(self.SINTONIZADOR)
        self._SINTONIZADOR_text_box.set_value(self.SINTONIZADOR)
        self.rtlsdr_source_0.set_center_freq(self.SINTONIZADOR, 0)

    def get_GANANCIA(self):
        return self.GANANCIA

    def set_GANANCIA(self, GANANCIA):
        self.GANANCIA = GANANCIA
        self._GANANCIA_slider.set_value(self.GANANCIA)
        self._GANANCIA_text_box.set_value(self.GANANCIA)
        self.rtlsdr_source_0.set_gain(self.GANANCIA, 0)


def main(top_block_cls=RECEPTOR_FM, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
