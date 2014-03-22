#!/usr/bin/env python
import sys, os
import struct


class NSFFileError(Exception):
    """geric NSFFile exception"""


class NSFFile(object):
    TYPE_NTSC = 'ntsc'
    TYPE_PAL = 'pal'
    TYPE_BOTH = 'both'

    TYPES = [TYPE_NTSC, TYPE_PAL, TYPE_BOTH]

    SC_VRCVI = 'vrcvi'
    SC_VRCVII = 'vrcvii'
    SC_FDS_SOUND = 'fds sound'
    SC_MMC5_AUDIO = 'mmc5 audio'
    SC_NAMCO_106 = 'namco 106'
    SC_SUNSOFT_FME_07 = 'sunsoft fme-07'

    SOUND_CHIPS = [SC_VRCVI, SC_VRCVII, SC_FDS_SOUND, SC_MMC5_AUDIO, SC_NAMCO_106, SC_SUNSOFT_FME_07]

    _struct_format = '<5scccHHH32s32s32sH8sHcc4s'
    _struct_len = struct.calcsize(_struct_format)
    _nsf_magic = 'NESM\x1A'

    def __init__(self, nsf_file):
        self.file_name = nsf_file
        try:
            with open(nsf_file) as f:
                data = f.read()
        except IOError as e:
            raise NSFFile('failed to read %s (%s)' % (nsf_file, str(e)))
        
        info = struct.unpack(self._struct_format, data[:self._struct_len])
        if info[0] != self._nsf_magic:
            raise NSFFileError('%s is not a valid NSF file' % nsf_file)

        self.nsf_version = ord(info[1])
        self.total_songs = ord(info[2])
        self.starting_song = ord(info[3])
        self.load_address = info[4]
        self.init_address = info[5]
        self.play_address = info[6]

        def from_c_str(in_str):
            loc = in_str.find('\x00')
            if loc == -1:
                return in_str
            return in_str[:loc]

        self.song_name = from_c_str(info[7])
        self.artist_name = from_c_str(info[8])
        self.copyright = from_c_str(info[9])
        self.ntsc_speed = info[10]
        self.bankswitch = info[11]
        self.pal_speed = info[12]
        self.ntsc_pal_bits = info[13]
        self.sound_chip_bits = info[14]

        ntsc_pal = bin(ord(self.ntsc_pal_bits))[2:].ljust(8, '0')
        if ntsc_pal[-2] == '1':
            self.tune_type = self.TYPE_BOTH
        elif ntsc_pal[-1] == '0':
            self.tune_type = self.TYPE_NTSC
        else:
            self.tune_type = self.TYPE_PAL

        self.extra_sound_chips = []

        for index, bit in enumerate(bin(ord(self.sound_chip_bits))[2:].ljust(8, '0')[-1:-6:-1]):
            if bit == '1':
                self.extra_sound_chips.append(self.SOUND_CHIPS[index])

        self.data = data[self._struct_len:]


    def print_info(self):
        print 'song name:     %s' % self.song_name
        print 'song artist:   %s' % self.artist_name
        print 'copyright:     %s' % self.copyright
        print 'total songs:   %d' % self.total_songs
        print 'starting song: %d' % self.starting_song
        print 'load address:  %d' % self.load_address
        print 'init address:  %d' % self.init_address
        print 'play address:  %d' % self.play_address
        print 'ntsc speed:    %d' % self.ntsc_speed
        print 'pal speed:     %d' % self.pal_speed
        print 'bankswitch:    0x%s' % self.bankswitch.encode('hex')
        print 'ntsc/pal bits: %s' % bin(ord(self.ntsc_pal_bits)).ljust(8, '0')
        print 'snd chip bits: %s' % bin(ord(self.sound_chip_bits)).ljust(8, '0')
        print 'tune type:     %s' % self.tune_type
        print 'extra chips:   %s' % ', '.join(self.extra_sound_chips)

        
        
if __name__ == '__main__':
    nsffile = NSFFile(sys.argv[1])
    nsffile.print_info()

