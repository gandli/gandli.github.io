---
title: rime
date: 2024-06-17 23:33:26
tags:
---

1. [rime](https://rime.im/download/)
2. [雾凇拼音](https://github.com/iDvel/rime-ice)


`weasel.custom.yaml`

```yaml
customization:
  distribution_code_name: Weasel
  distribution_version: 0.16.1
  generator: "Weasel::UIStyleSettings"
  modified_time: "Fri Jun 14 23:23:21 2024"
  rime_version: 1.11.2
patch:
  preset_color_schemes:
    weType_dark:
      {
        author: wechat,
        back_color: 0x000000,
        border_color: 0x000000,
        comment_text_color: 0x999999,
        hilited_candidate_back_color: 0x75B100,
        hilited_candidate_text_color: 0xFFFFFF,
        hilited_label_color: 0xFFFFFF,
        label_color: 0x424242,
        name: "微信输入法weTypeDark",
        shadow_color: 0x20000000,
        text_color: 0xCCCCCC,
      }
    weType_light:
      {
        author: wechat,
        back_color: 0xFFFFFF,
        border_color: 0xFFDBDBDB,
        comment_text_color: 0x999999,
        hilited_candidate_back_color: 0x75B100,
        hilited_candidate_text_color: 0xFFFFFF,
        hilited_label_color: 0xFFFFFF,
        label_color: 0x888888,
        name: "微信输入法weTypeLight",
        shadow_color: 0x20000000,
        text_color: 0x333333,
      }
  style:
    candidate_format: "%c\u2005%@\u2005"
    color_scheme: weType_light
    color_scheme_dark: weType_dark
    font_face: "霞鹜文楷 GB,苹方,PingFangSC,微软雅黑"
    font_point: 14
    horizontal: true
    inline_preedit: true
    label_font_point: 10
    layout:
      {
        align_type: center,
        border: 1,
        back_radius: 10,
        corner_radius: 10,
        candidate_spacing: 11,
        hilite_padding: 2,
        hilite_padding_x: 7,
        hilite_spacing: 3,
        hilited_corner_radius: 10,
        margin_x: 12,
        margin_y: 8,
        round_corner: 10,
        shadow_radius: 5,
        spacing: 0,
      }
  "style/color_scheme": weType_light
```


