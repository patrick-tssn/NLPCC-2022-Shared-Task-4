# NLPCC-2022-Shared-Task-4
Multimodal Dialogue Understanding and Generation

## [NLPCC'22 Shared Task 4](http://tcci.ccf.org.cn/conference/2022/cfpt.php)

### Data

#### Statistics

|       | clips  | utterances | scenes | sessions | utter/clip | scene/clip | session/clip | en_word/clip | en_word/utter | ch_word/clip | ch_word/utter |
| ----- | ------ | ---------- | ------ | -------- | ---------- | ---------- | ------------ | ------------ | ------------- | ------------ | ------------- |
| train | 40,006 | 1,000,079  | 56,535 | 106,078  | 25         | 1.41       | 2.65         | 166.46       | 6.66          | 267.74       | 10.71         |
| valid | 1,955  | 50,032     | 3,202  | 6,331    | 25.6       | 1.64       | 3.24         | 174.49       | 6.82          | 283.7        | 11.09         |
| test  | 1,934  | 50,131     | 3,284  | 6,949    | 25.92      | 1.7        | 3.59         | 178.65       | 6.89          | 286.42       | 11.05         |

#### Detail
Download `[train|valid].jsonl and MDUG_rgb_[train|valid]_n.zip`  [BaiduNetDisk](https://pan.baidu.com/s/1yTVtZB5bgGN_wNvJw0_JbQ?pwd=xg56 ) | GoogleDrive
- TEXT

```
# .jsonl
{'Safe_S01E05': // [name of TV show]_S[season]_E[episode]
       [{
            'vid':'Safe_S01E05_clip_000', // clip id
            'subs':[
                {
                    'turn_id':0, // turn id of current clip
                    'en_text':'', // English
                    'ch_text':'', // Chinese
                    'start':0.00, // start time of the utterance in the clip
                    'end':0.00, // end time of the utterance in the clip
                    'scene':1, // 1: start of new dialog scene; 0: otherwise
                    'session':1 // 1: start of new dialog session; 0: otherwise
                }, 
                ...]
        }, 
        ...]
 }
 ...
```

- VIDEO

NOTE: We only provide frames(3fps) of provided utterances

```
// [name of TV show]_S[season]_E[episode]_clip_[clip id]_dia_[turn id]_[image id].jpg
├──Safe
      └── Safe_S01E01
            └── clip_000
                     └── Safe_S01E01_clip_000_dia_00_01.jpg 
                     └── Safe_S01E01_clip_000_dia_00_02.jpg
                     └── ...
            └── ...
      └── ...
 ├── ...
```



### Overview

◇ Task 4 - Multimodal Dialogue Understanding and Generation

The multimodal dialogue understanding and generation task can be divided into two phases: multimodal context understanding and response generation. Specifically, the former includes dialogue session identification (i.e., determining whether the dialogue content has changed) and dialogue scene identification (i.e., determining whether the video context has changed). The ultimate goal is to generate a response that is coherent to the dialogue context and relevant to the video context. This task includes three tracks:

● Track 1: Dialogue scene identification: predict the boundaries of different dialogue scenes given a set of continuous dialogue utterances and a related video.

● Track 2: Dialogue session identification: predict the boundaries of different dialogue sessions given a set of continuous dialogue utterances and a related video (which is identical to Track 1).

● Track 3: Dialogue response generation: generate a response based on scene and session predictions, while coherently catching up with the conversation.

Organizer: Wangxuan Institute of Computer Technology, Peking University

Contact: Xueliang ZHAO ([xl.zhao@pku.edu.cn](mailto:xl.zhao@pku.edu.cn))
