# #!/usr/bin/env python

# # Python wrapper for METEOR implementation, by Xinlei Chen
# # Acknowledge Michael Denkowski for the generous discussion and help 

# import os
# import sys
# import subprocess
# import threading

# from signal import signal, SIGPIPE, SIG_DFL
# signal(SIGPIPE,SIG_DFL) 

# # Assumes meteor-1.5.jar is in the same directory as meteor.py.  Change as needed.
# METEOR_JAR = 'meteor-1.5.jar'
# # print METEOR_JAR

# class Meteor:

#     def __init__(self):
#         self.meteor_cmd = ['java', '-jar', '-Xmx2G', METEOR_JAR, \
#                 '-', '-', '-stdio', '-l', 'en', '-norm']
#         self.meteor_p = subprocess.Popen(self.meteor_cmd, \
#                 cwd=os.path.dirname(os.path.abspath(__file__)), \
#                 stdin=subprocess.PIPE, \
#                 stdout=subprocess.PIPE, \
#                 stderr=subprocess.PIPE)
#         # Used to guarantee thread safety
#         self.lock = threading.Lock()

#     def compute_score(self, gts, res):
#         assert(gts.keys() == res.keys())
#         imgIds = gts.keys()
#         scores = []

#         eval_line = 'EVAL'
#         self.lock.acquire()
#         for i in imgIds:
#             assert(len(res[i]) == 1)
#             stat = self._stat(res[i][0], gts[i])
#             eval_line += ' ||| {}'.format(stat)

#         self.meteor_p.stdin.write('{}\n'.format(eval_line))
#         for i in range(0,len(imgIds)):
#             scores.append(float(self.meteor_p.stdout.readline().strip()))
#         score = float(self.meteor_p.stdout.readline().strip())
#         self.lock.release()

#         return score, scores

#     def method(self):
#         return "METEOR"

#     def _stat(self, hypothesis_str, reference_list):
#         # SCORE ||| reference 1 words ||| reference n words ||| hypothesis words
#         hypothesis_str = hypothesis_str.replace('|||','').replace('  ',' ')
#         # score_line = ' ||| '.join(('SCORE', ' ||| '.join(reference_list), hypothesis_str))
#         # self.meteor_p.stdin.write('{}\n'.format(score_line).encode('utf-8'))
#         # return self.meteor_p.stdout.readline().strip()
#         if sys.version_info[0] == 2:  # python2
#             score_line = ' ||| '.join(('SCORE', ' ||| '.join(reference_list), hypothesis_str)).encode('utf-8').strip()
#             self.meteor_p.stdin.write(str(score_line+b'\n'))
#         else:  # assume python3+
#             score_line = ' ||| '.join(('SCORE', ' ||| '.join(reference_list), hypothesis_str)).strip()
#             # self.meteor_p.stdin.write(score_line+'\n')
#             self.meteor_p.stdin.write((score_line+'\n').encode('utf-8'))
#         return self.meteor_p.stdout.readline().strip()

#     def _score(self, hypothesis_str, reference_list):
#         self.lock.acquire()
#         # SCORE ||| reference 1 words ||| reference n words ||| hypothesis words
#         hypothesis_str = hypothesis_str.replace('|||','').replace('  ',' ')
#         score_line = ' ||| '.join(('SCORE', ' ||| '.join(reference_list), hypothesis_str))
#         self.meteor_p.stdin.write('{}\n'.format(score_line))
#         stats = self.meteor_p.stdout.readline().strip()
#         eval_line = 'EVAL ||| {}'.format(stats)
#         # EVAL ||| stats 
#         self.meteor_p.stdin.write('{}\n'.format(eval_line))
#         score = float(self.meteor_p.stdout.readline().strip())
#         # bug fix: there are two values returned by the jar file, one average, and one all, so do it twice
#         # thanks for Andrej for pointing this out
#         score = float(self.meteor_p.stdout.readline().strip())
#         self.lock.release()
#         return score
 
#     def __del__(self):
#         self.lock.acquire()
#         self.meteor_p.stdin.close()
#         self.meteor_p.kill()
#         self.meteor_p.wait()
#         self.lock.release()

# adapt file
#!/usr/bin/env python

# Python wrapper for METEOR implementation, by Xinlei Chen
# Acknowledge Michael Denkowski for the generous discussion and help 
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
import subprocess
import threading

# Assumes meteor-1.5.jar is in the same directory as meteor.py.  Change as needed.
METEOR_JAR = 'meteor-1.5.jar'
# print METEOR_JAR

class Meteor:

    def __init__(self):
        self.env = os.environ
        self.env['LC_ALL'] = 'en_US.UTF_8'
        self.meteor_cmd = ['java', '-jar', '-Xmx2G', METEOR_JAR,
                '-', '-', '-stdio', '-l', 'en', '-norm']
        self.meteor_p = subprocess.Popen(self.meteor_cmd,
                cwd=os.path.dirname(os.path.abspath(__file__)),
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=self.env, universal_newlines=True, bufsize=1)
        # Used to guarantee thread safety
        self.lock = threading.Lock()

    def compute_score(self, gts, res):
        assert(gts.keys() == res.keys())
        imgIds = sorted(list(gts.keys()))
        scores = []

        eval_line = 'EVAL'
        self.lock.acquire()
        for i in imgIds:
            assert(len(res[i]) == 1)
            # There's a situation that the prediction is all punctuations
            # (see definition of PUNCTUATIONS in pycocoevalcap/tokenizer/ptbtokenizer.py)
            # then the prediction will become [''] after tokenization
            # which means res[i][0] == '' and self._stat will failed with this input
            if len(res[i][0]) == 0:
                res[i][0] = 'a'
            stat = self._stat(res[i][0], gts[i])
            eval_line += ' ||| {}'.format(stat)

        # Send to METEOR
        self.meteor_p.stdin.write(eval_line + '\n')
        
        # Collect segment scores
        for i in range(len(imgIds)):
            score = float(self.meteor_p.stdout.readline().strip())
            scores.append(score)

        # Final score
        final_score = float(self.meteor_p.stdout.readline().strip())
        self.lock.release()

        return final_score, scores

    def method(self):
        return "METEOR"

    def _stat(self, hypothesis_str, reference_list):
        # SCORE ||| reference 1 words ||| reference n words ||| hypothesis words
        hypothesis_str = hypothesis_str.replace('|||', '').replace('  ', ' ')
        if sys.version_info[0] == 2:  # python2
            score_line = ' ||| '.join(('SCORE', ' ||| '.join(reference_list), hypothesis_str)).encode('utf-8').strip()
            self.meteor_p.stdin.write(str(score_line+b'\n'))
        else:  # assume python3+
            score_line = ' ||| '.join(('SCORE', ' ||| '.join(reference_list), hypothesis_str)).strip()
            self.meteor_p.stdin.write(score_line+'\n')
        return self.meteor_p.stdout.readline().strip()
 
    def __del__(self):
        self.lock.acquire()
        self.meteor_p.stdin.close()
        self.meteor_p.kill()
        self.meteor_p.wait()
        self.lock.release()