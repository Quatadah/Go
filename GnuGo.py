import subprocess, sys

''' Connection with the Go Text Protocol of GNU Go.
You have to have gnugo installed, and in your exec path.'''
import random

class GnuGo():

    def query(self, s):
        self._stdin.write(s + "\n")
        ret = []
        while True:
            l = self._stdout.readline().rstrip()
            if l == "":
                break
            ret.append(l)
        if len(ret) == 1 and ret[0].startswith('='):
            return ('OK', ret[0][1:])
        elif len(ret) == 0:
            return ('NOK', None)
        else:
            return ('NOK', ret[0])

    def __str__(self):
        self._stdin.write("showboard\n")
        ret = []
        while True:
            l = self._stdout.readline().rstrip()
            if l == "":
                break
            ret.append(l)
        return "\n".join(ret[1:])

    def finalScore(self):
        self._stdin.write("final_score\n")
        ret = []
        while True:
            l = self._stdout.readline().rstrip()
            if l == "":
                break
            ret.append(l)
        return ret[0][2:]

    class Moves():
        
        def __init__(self, gnugo):
            self._nextplayer = "black"
            self._gnugo = gnugo

        def flip(self):
            if self._nextplayer == "black":
                self._nextplayer = "white"
            else:
                self._nextplayer = "black"

        def player(self):
            return self._nextplayer

        def getbest(self):
            status, toret = self._gnugo.query("reg_genmove " + self._nextplayer)
            if status == "OK":
                return toret.strip()
            return "ERR"

        def get_randomized_best(self):
            status, toret = self._gnugo.query("experimental_score " + self._nextplayer)
            if status != "OK":
                return "ERR"
            status, toret = self._gnugo.query("top_moves " + self._nextplayer)
            if status != "OK":
                return "ERR"
            moves = []
            scoremoves = []
            cumulatedscore = []
            cumul = 0
            toread = toret.strip().split()
            if len(toread) == 0:
                return "PASS"
            while len(toread) > 0:
                m = toread.pop(0)
                s = float(toread.pop(0))
                moves.append(m)
                scoremoves.append(s)
                cumul += s
                cumulatedscore.append(cumul)
            r = random.uniform(0,cumul)
            i = 0
            while i < len(moves) and r > cumulatedscore[i]:
                i += 1
            if i >= len(moves):
                i = len(moves) -1
            return moves[i]

        def get_history(self):
            status, toret = self._gnugo.query("move_history")
            if status != "OK":
                return "ERR"
            toread = toret.strip().split()
            return toread

        def playthis(self, move):
            status, toret = self._gnugo.query("play " + self._nextplayer + " " + str(move))
            #print(status, toret)
            self.flip()
            return status

        def __iter__(self):
            return self

        def __next__(self):
            status, toret = self._gnugo.query("genmove " + self._nextplayer)
            self.flip()
            if status=="OK":
                return toret.strip()
            return "ERR"

    def __init__(self, size):
        self._proc = subprocess.Popen(['gnugo', '--capture-all-dead', '--chinese-rules', '--boardsize',str(size), '--mode', 'gtp', '--never-resign', '--seed', '0'], bufsize = 1, stdin=subprocess.PIPE,
                stdout=subprocess.PIPE, universal_newlines=True)
        self._stdin = self._proc.stdin
        self._stdout = self._proc.stdout
        self._size = size
        self._nextplayer = "black"
        (ok, _) = self.query("level 0")
        assert ok=='OK'
        (ok, _) = self.query("boardsize "+str(size))
        assert ok=='OK'
        (ok, _) = self.query("clear_board")
        assert ok=='OK'
        (ok, name) = self.query("name")
        assert ok=='OK'
        (ok, version) = self.query("version")
        assert ok=='OK'
        #print("Connection to", name.strip(), "(" + version.strip() + ")","Ok")
        (ok, legal) = self.query("all_legal black")
        assert ok=='OK'
        #print("Legal moves: ", legal)
        
