# NLPCC-2022-Shared-Task-4
Multimodal Dialogue Understanding and Generation

*Please refer to the latest shared task: [NLPCC2023 Shared Task 10](https://github.com/yellow-binary-tree/NLPCC-2023-Shared-Task-10)*

## [Overview](http://tcci.ccf.org.cn/conference/2022/cfpt.php)

◇ Task 4 - Multimodal Dialogue Understanding and Generation

The multimodal dialogue understanding and generation task can be divided into two phases: multimodal context understanding and response generation. Specifically, the former includes dialogue session identification (i.e., determining whether the dialogue content has changed) and dialogue scene identification (i.e., determining whether the video context has changed). The ultimate goal is to generate a response that is coherent to the dialogue context and relevant to the video context. This task includes three tracks:

● Track 1: Dialogue scene identification: predict the boundaries of different dialogue scenes given a set of continuous dialogue utterances and a related video.

● Track 2: Dialogue session identification: predict the boundaries of different dialogue sessions given a set of continuous dialogue utterances and a related video (which is identical to Track 1).

● Track 3: Dialogue response generation: generate a response based on scene and session predictions, while coherently catching up with the conversation.

Organizer: Wangxuan Institute of Computer Technology, Peking University


## Data

### Statistics

|       | clips  | utterances | scenes | sessions | utter/clip | scene/clip | session/clip | en_word/clip | en_word/utter | ch_word/clip | ch_word/utter |
| ----- | ------ | ---------- | ------ | -------- | ---------- | ---------- | ------------ | ------------ | ------------- | ------------ | ------------- |
| train | 40,006 | 1,000,079  | 56,535 | 106,078  | 25         | 1.41       | 2.65         | 166.46       | 6.66          | 267.74       | 10.71         |
| valid | 1,955  | 50,032     | 3,202  | 6,331    | 25.6       | 1.64       | 3.24         | 174.49       | 6.82          | 283.7        | 11.09         |
| test  | 1,934  | 50,131     | 3,284  | 6,949    | 25.92      | 1.7        | 3.59         | 178.65       | 6.89          | 286.42       | 11.05         |

### LeaderBoard

#### Track 1
| Team ID  | Accuracy | F1    |
| -------- | -------- | ----- |
| LingJing | 93.88    | 18.15 |
|          |          |       |

#### Track 2
| Team ID  | Accuracy | F1    |
| -------- | -------- | ----- |
| LingJing | 87.79    | 28.90 |
| Eastwood | 72.29    | 39.76 |
|          |          |       |

#### Track 3
| Team ID  | Bleu1 | Bleu2 | Bleu3 | Bleu4 | Rouge-L | METEOR | CIDEr |
| -------- | ----- | ----- | ----- | ----- | ------- | ------ | ----- |
| LingJing | 0.139 | 0.100 | 0.083 | 0.072 | 0.226   | 0.117  | 1.290 |
|          |       |       |       |       |         |        |       |





### UPDATE

#### 2022.05.23 We released the evaluation scripts

evaluation/evaluate.py

#### 2022.05.12 We released the test set, you can download from [BaiduNetDisk(closed)]()

*SUBMISSION FORMAT:*

```
#
# task 1: TEAMID_track1.json
{
       'Friends_S01E01_clip_000':[1, 0, ...], # your prediction in list format(you are not asked to predict the label of the last utterance.)
       ...
}
# task 2: TEAMID_track2.json
{
       'Friends_S01E01_clip_000':[1, 0, ...], # your prediction in list format(you are not asked to predict the label of the last utterance.)
       ...
}
# task 3: TEAMID_track3.json
{
       'Friends_S01E01_clip_000':'__ANSWER__', # replace __ANSWER__ with your answer(English only)
       ...
}
```
SUBMISSION Deadline: 2022.05.20

SUBMISSION ENTRY(closed)

### Details
Download `[train|valid].jsonl and MDUG_rgb_[train|valid]_n.zip`  [BaiduNetDisk(closed)]() | [GoogleDrive(closed)]()
- TEXT

```
# .jsonl
{'Friends_S01E01': // episode id: [name of TV show]_S[season]_E[episode]
       [{
            'vid':'Friends_S01E01_clip_000', // clip id
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

*NOTE:* We only provide frames(3fps) of the provided utterances

```
// [name of TV show]_S[season]_E[episode]_clip_[clip id]_dia_[turn id]_[image id].jpg
├── Friends_S01E01
     └── clip_000
              └── Friends_S01E01_clip_000_dia_00_01.jpg 
              └── Friends_S01E01_clip_000_dia_00_02.jpg
              └── ...
     └── ...
├── ...
```
```
// MD5
{
       "MDUG_rgb_train_1.zip": "746ce538d0568f190659084c908d7de0", 
       "MDUG_rgb_train_2.zip": "9413810d1d1c9332376b08cf4fd7c037", 
       "MDUG_rgb_train_3.zip": "5247a69664dd9089f6801bcba32bc036", 
       "MDUG_rgb_train_4.zip": "934265252eaba3df98806fd9755b8a1e", 
       "MDUG_rgb_train_5.zip": "6c35c52733ff50fa868523abb237771b", 
       "MDUG_rgb_train_6.zip": "1d0c508569d3f56cac2d263ba7f419f6", 
       "MDUG_rgb_train_7.zip": "5208ac23a7f674ff5640466878b70669", 
       "MDUG_rgb_train_8.zip": "bc988d145bc6f940a7e0f64b5da69685", 
       "MDUG_rgb_train_9.zip": "d451cfe63f1db914bc9f6d4041c3f897", 
       "MDUG_rgb_train_10.zip": "0bd60f108da36e301882f7b30ad77233", 
       "MDUG_rgb_train_11.zip": "abedefadcda2998e4cd1c6563c62e182", 
       "MDUG_rgb_train_12.zip": "e114d158b456339bbb9fc6a0a32be56a", 
       "MDUG_rgb_train_13.zip": "2faddea5401d7b191e0155bb20350280", 
       "MDUG_rgb_train_14.zip": "c68ce06a7a3c6c8466f4484b04682d16", 
       "MDUG_rgb_train_15.zip": "96909cf7a7aa6b3780dae90e6a703f9c", 
       "MDUG_rgb_train_16.zip": "0ffd572468c8f8255aa16dcf25d20b7d"
}
{
       "MDUG_rgb_valid.zip": "1e00d0ba50dc7fdb41f12936500a7de7"
}
```



