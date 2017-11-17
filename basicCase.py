# ------------------- basic cases for daily--------------------

BasicCase4DualBand = [
    # wifi basic
    "AP_CLEAR_CHAN",
    [
        "assoc_lan_wifi_2g",
        "assoc_lan_wifi_5g",
        "assoc_clear_sta_2g",
        "assoc_clear_sta_5g",
    ],
    'AP_CLEAR_LOW',
    [
        "assoc_clear_sta_2g",
        "assoc_clear_sta_5g",
    ],
    'AP_CLEAR_HIGH',
    [
        "assoc_clear_sta_2g",
        "assoc_clear_sta_5g",
    ],
    "AP_CLEAR_LOW_TXPOWER",
    [
        "autochan_txpower_2g",
        "autochan_txpower_5g",
    ],
    "AP_CLEAR_MID_TXPOWER",
    [
        "autochan_txpower_2g",
        "autochan_txpower_5g",
    ],
    "AP_CLEAR_HIGH_TXPOWER",
    [
        "autochan_txpower_2g",
        "autochan_txpower_5g",
    ],
    "AP_CLEAR_CHANSELECTION",
    [
        "chanselection_2g",
        "chanselection_5g",
    ],
    "AP_MIXEDPSK_CHAN_CHECK",
    [
        "chan1_check_2g",
        "chan6_check_2g",
        "chan11_check_2g",
        "chan13_check_2g",
        "chan36_check_5g",
        "chan52_check_5g",
        "chan157_check_5g",
        "chan165_check_5g",
    ],
    'AP_PSK2_CHAN',
    [
        'assoc_psk2_sta_2g',
        'assoc_psk2_sta_5g',
    ],
    'AP_MIXEDPSK_BW_CHECK',
    [
        'autochan_BW_check_2g',
        'autochan_BW_check_5g',
        'chan1_BW40_CHECK_2g',
        'chan11_BW40_CHECK_2g',
        'chan13_BWauto_CHECK_2g',
        'chan36_BW20_CHECK_5g',
        'chan52_BW80_CHECK_5g',
        'chan157_BW40_CHECK_5g',
        'chan165_BWauto_CHECK_5g',
    ],
    'AP_MIXEDPSK_CHAN',
    [
        'assoc_router_ping_psk2_2g',
        'assoc_tkippsk_sta_2g',
        'assoc_router_ping_psk2_5g',
        'assoc_tkippsk_sta_5g',
    ],
    'AP_MIXEDPSK_CHAN_BW40',
    [
        "assoc_psk2_sta_5g",
        "assoc_tkippsk_sta_5g",
        "assoc_psk2_sta_2g",
        "assoc_tkippsk_sta_2g"
    ],
    'AP_MIXEDPSK_CHAN_BW20',
    [
        "assoc_psk2_sta_2g",
        "assoc_tkippsk_sta_2g",
        "assoc_psk2_sta_5g",
        "assoc_tkippsk_sta_5g",
    ],
    "AP_MIXEDPSK_CHAN_SSIDSPEC",
    [
        'assoc_psk2_sta_ssidspec_2g',
        'assoc_psk2_sta_ssidspec_5g',
    ],
    "AP_MIXEDPSK_CHAN_KEYSPEC",
    [
        'assoc_psk2_sta_keyspec_2g',
        'assoc_psk2_sta_keyspec_5g',
    ],
    "AP_MIXEDPSK_CHAN_SSIDCHINESE",
    [
        "assoc_psk2_sta_ssidchinese_2g",
        'assoc_psk2_sta_ssidchinese_5g',
    ],
    'AP_SSIDHIDE_CHECK',
    [
        'ap_mixedpsk_ssidhide_2g',
        'ap_mixedpsk_ssidhide_5g',
    ],
    'AP_MIXEDPSK_SSIDHIDE',
    [
        'assoc_psk2_sta_2g',
        'assoc_psk2_sta_5g',
    ],

    # guest
    'AP_GUEST_CLEAR',
    [
        'assoc_clear_sta_guest',
    ],
    'AP_GUEST_PSK2',
    [
        'assoc_psk2_sta_guest',
    ],
    'AP_GUEST_MIXEDPSK',
    [
        'assoc_psk2_sta_guest',
    ],

    # wps
    'AP_WPS',
    [
        'assoc_wps'
    ],

    # bsd
    'AP_MIXEDPSK_BSD',
    [
        'assoc_psk2_near_field_sta',
    ],

    # qos
    'AP_QOS_MIXEDPSK',
    [
        'assoc_psk2_sta_speedtest_2g',
        'assoc_psk2_sta_speedtest_5g',
     ],
    'AP_QOS_GUEST_MIXEDPSK',
    [
        'assoc_psk2_sta_speedtest_guest'
    ],
    'AP_QOS_ROUTERSELF',
    [
        'routerSelf_speedtest'
    ],

    # white/black list
    'AP_CLEAR_CHAN_WHITELIST',
    [
        'assoc_clear_sta_in_whitelist_2g',
        'assoc_clear_sta_outof_whitelist_2g',
        'assoc_clear_sta_in_whitelist_5g',
        'assoc_clear_sta_outof_whitelist_5g',
    ],
    'AP_CLEAR_CHAN_BLACKLIST',
    [
        'assoc_clear_sta_in_blacklist_2g',
        'assoc_clear_sta_outof_blacklist_2g',
        'assoc_clear_sta_in_blacklist_5g',
        'assoc_clear_sta_outof_blacklist_5g',
    ],

    # internetAccessControl
    'AP_MIXEDPSK_NET_FORBIDDEN',
    [
        'assoc_psk2_netForbidden_2g',
        'assoc_psk2_netForbidden_5g',
        'assoc_psk2_netForbidden_off_2g',
        'assoc_psk2_netForbidden_off_5g'
    ],

    # wire Relay
    'AP_RELAY_CONFIG_CHECK',
    [
        'wire_relay_ping_UpperRouter',
        'wire_relay_ping_internet',
        'wifi_config_check_2g',
        'wifi_config_check_5g',
        'wifi_config_check_guest'
    ],
    'AP_RELAY_STA_ONLINE',
    [
        'assoc_clear_chan1_2g',
        'assoc_clear_chan36_5g',
        'assoc_psk2_chan6_2g',
        'assoc_psk2_chan52_5g',
        'assoc_mixed_chan11_2g',
        'assoc_mixed_chan149_5g'
    ],

    # 2g wireless relay
    'AP_WIRELESS_RELAY_2G',
    [
        'wifiRelay_switchCheck_2g',
        'config_check_5g',
        'config_check_guest',
        'config_check_2g',
        'assoc_afterModeChange_2g',
        'assoc_afterModeChange_5g',
    ],

    # 5g wireless relay
    'AP_WIRELESS_RELAY_5G',
    [
        'wifiRelay_switchCheck_5g',
        'config_check_2g',
        'config_check_guest',
        'config_check_5g',
        'assoc_afterModeChange_2g',
        'assoc_afterModeChange_5g',
    ],
]

