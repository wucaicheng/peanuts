# ------------------- data for the treectrl--------------------
# when change treeApi, must change processreport.GetTestModule
treeBasicApi = [
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
    'AP_CLEAR_MID',
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
        "chan1_txpower_2g",
        "chan6_txpower_2g",
        "chan11_txpower_2g",
        "chan13_txpower_2g",
        "chan36_txpower_5g",
        "chan52_txpower_5g",
        "chan149_txpower_5g",
        "chan165_txpower_5g",
    ],
    "AP_CLEAR_MID_TXPOWER",
    [
        "autochan_txpower_2g",
        "autochan_txpower_5g",
        "chan1_txpower_2g",
        "chan6_txpower_2g",
        "chan11_txpower_2g",
        "chan13_txpower_2g",
        "chan36_txpower_5g",
        "chan52_txpower_5g",
        "chan149_txpower_5g",
        "chan165_txpower_5g",
    ],
    "AP_CLEAR_HIGH_TXPOWER",
    [
        "autochan_txpower_2g",
        "autochan_txpower_5g",
        "chan1_txpower_2g",
        "chan6_txpower_2g",
        "chan11_txpower_2g",
        "chan13_txpower_2g",
        "chan36_txpower_5g",
        "chan52_txpower_5g",
        "chan149_txpower_5g",
        "chan165_txpower_5g",
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
        "chan44_check_5g",
        "chan52_check_5g",
        "chan60_check_5g",
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
        'chan6_BW20_CHECK_2g',
        'chan11_BW40_CHECK_2g',
        'chan13_BWauto_CHECK_2g',
        'chan36_BW20_CHECK_5g',
        'chan48_BW40_CHECK_5g',
        'chan52_BW80_CHECK_5g',
        'chan64_BW20_CHECK_5g',
        'chan157_BW40_CHECK_5g',
        'chan165_BWauto_CHECK_5g',
    ],
    'AP_MIXEDPSK_CHAN',
    [
        'assoc_router_ping_psk2_2g',
        'assoc_psk_sta_2g',
        'assoc_tkippsk2_sta_2g',
        'assoc_tkippsk_sta_2g',
        'assoc_router_ping_psk2_5g',
        'assoc_psk_sta_5g',
        'assoc_tkippsk2_sta_5g',
        'assoc_tkippsk_sta_5g',
    ],
    'AP_MIXEDPSK_CHAN_BW40',
    [
        "assoc_psk2_sta_5g",
        "assoc_psk_sta_5g",
        "assoc_tkippsk2_sta_5g",
        "assoc_tkippsk_sta_5g",
        "assoc_psk2_sta_2g",
        "assoc_psk_sta_2g",
        "assoc_tkippsk2_sta_2g",
        "assoc_tkippsk_sta_2g"
    ],
    'AP_MIXEDPSK_CHAN_BW20',
    [
        "assoc_psk2_sta_2g",
        "assoc_psk_sta_2g",
        "assoc_tkippsk2_sta_2g",
        "assoc_tkippsk_sta_2g",
        "assoc_psk2_sta_5g",
        "assoc_psk_sta_5g",
        "assoc_tkippsk2_sta_5g",
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
        'ap_clear_ssidhide_2g',
        'ap_clear_ssidhide_5g',
        'ap_psk2_ssidhide_2g',
        'ap_psk2_ssidhide_5g',
        'ap_mixedpsk_ssidhide_2g',
        'ap_mixedpsk_ssidhide_5g',
    ],
    'AP_MIXEDPSK_SSIDHIDE',
    [
        'assoc_psk2_sta_2g',
        'assoc_psk2_sta_5g',
    ],
]

treeWpsApi = [
    'AP_WPS',
    [
        'assoc_wps'
    ]
]

treeGuestWifiApi = [
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
        'assoc_psk_sta_guest',
        'assoc_tkippsk2_sta_guest',
        'assoc_tkippsk_sta_guest',
    ],
]


treeBSDApi = [
    'AP_CLEAR_BSD',
    [
        'assoc_clear_near_field_sta',
    ],
    'AP_MIXEDPSK_BSD',
    [
        'assoc_psk2_near_field_sta',
        'assoc_psk2_near_field_sta_repeat',
        # 'assoc_psk_near_field_sta',
        # 'assoc_tkippsk2_near_field_sta',
        # 'assoc_tkippsk_near_field_sta',
    ],
    'AP_BSD_CHAN_CHECK',
    [
        'chan_1_36_check_bsd',
        'chan_6_52_check_bsd',
        'chan_13_165_check_bsd',
    ],
    'AP_BSD_BW_CHECK',
    [
        'autochan_BW_check_bsd',
        'chan6_48_BW40_20_check_bsd',
        'chan13_64_BW20_40_check_bsd',
    ],
    # 'AP_MIXEDPSK_BSD_SSIDSPEC',
    # [
    #     'assoc_psk2_near_field_sta',
    #     'assoc_psk_near_field_sta',
    #     'assoc_tkippsk2_near_field_sta',
    #     'assoc_tkippsk_near_field_sta',
    # ],
    # 'AP_MIXEDPSK_BSD_KEYSPEC',
    # [
    #     'assoc_psk2_near_field_sta',
    #     'assoc_psk_near_field_sta',
    #     'assoc_tkippsk2_near_field_sta',
    #     'assoc_tkippsk_near_field_sta',
    # ],
    # 'AP_MIXEDPSK_BSD_SSIDCHINESE',
    # [
    #     'assoc_psk2_near_field_sta',
    #     'assoc_psk_near_field_sta',
    #     'assoc_tkippsk2_near_field_sta',
    #     'assoc_tkippsk_near_field_sta',
    # ],
    # 'AP_BSD_SSIDHIDE',
    # [
    #     'ap_clear_ssidhide',
    #     'ap_psk2_ssidhide',
    #     'ap_mixedpsk_ssidhide',
    # ],
    # 'AP_MIXEDPSK_BSD_SSIDHIDE',
    # [
    #     'assoc_psk2_near_field_sta',
    #     'assoc_psk_near_field_sta',
    #     'assoc_tkippsk2_near_field_sta',
    #     'assoc_tkippsk_near_field_sta'
    # ],
    # 'AP_MIXEDPSK_BSD_WHITELIST',
    # [
    #     'assoc_psk2_near_field_sta_in_whitelist',
    #     'assoc_psk2_near_field_sta_outof_whitelist',
    # ],
    # 'AP_MIXEDPSK_BSD_BLACKLIST',
    # [
    #     'assoc_psk2_near_field_sta_in_blacklist',
    #     'assoc_psk2_near_field_sta_outof_blacklist',
    # ],
    # 'AP_RELAY_MIXEDPSK_BSD',
    # [
    #     'assoc_psk2_near_field_sta',
    #     'assoc_psk_near_field_sta',
    #     'assoc_tkippsk2_near_field_sta',
    #     'assoc_tkippsk_near_field_sta',
    # ],
    # 'AP_RELAY_BSD_SSIDHIDE',
    # [
    #     'ap_clear_ssidhide',
    #     'ap_psk2_ssidhide',
    #     'ap_mixedpsk_ssidhide',
    # ],
    # 'AP_RELAY_MIXEDPSK_BSD_SSIDHIDE',
    # [
    #     'assoc_psk2_near_field_sta',
    #     'assoc_psk_near_field_sta',
    #     'assoc_tkippsk2_near_field_sta',
    #     'assoc_tkippsk_near_field_sta',
    # ],
    # 'AP_WIRELESS_RELAY_MIXEDPSK_BSD',
    # [
    #     'assoc_psk2_near_field_sta',
    #     'assoc_psk_near_field_sta',
    #     'assoc_tkippsk2_near_field_sta',
    #     'assoc_tkippsk_near_field_sta',
    # ],
    # 'AP_WIRELESS_RELAY_BSD_SSIDHIDE',
    # [
    #     'ap_clear_ssidhide',
    #     'ap_psk2_ssidhide',
    #     'ap_mixedpsk_ssidhide',
    # ],
    # 'AP_WIRELESS_RELAY_MIXEDPSK_BSD_SSIDHIDE',
    # [
    #     'assoc_psk2_near_field_sta',
    #     'assoc_psk_near_field_sta',
    #     'assoc_tkippsk2_near_field_sta',
    #     'assoc_tkippsk_near_field_sta',
    # ],
]

treeMUMIMOApi = [
    'AP_MUMIMO',
    [
        'MUMIMO_check',
        'assoc_noMUMIMO_5g',
    ],
]

treeWireRelayApi = [
    'AP_RELAY_CONFIG_CHECK',
    [
        'wan_port_belong_brlan',
        'wire_relay_ping_UpperRouter',
        'wire_relay_ping_internet',
        'wifi_config_check_2g',
        'wifi_config_check_5g',
        'wifi_config_check_guest',
        'autochan_txpower_min_2g',
        'autochan_txpower_mid_5g',
        'chan1_txpower_max_2g',
        'chan6_txpower_min_2g',
        'chan11_txpower_mid_2g',
        'chan13_txpower_max_2g',
        'chan36_txpower_min_5g',
        'chan52_txpower_mid_5g',
        'chan149_txpower_max_5g',
        'chan165_txpower_min_5g',
        'chanselection_2g',
        'chanselection_5g',
    ],
    'AP_RELAY_STA_ONLINE',
    [
        'assoc_clear_chan1_2g',
        'assoc_clear_chan36_5g',
        'assoc_psk2_chan6_2g',
        'assoc_psk2_chan52_5g',
        'assoc_mixed_chan11_2g',
        'assoc_mixed_chan149_5g',
        'assoc_mixed_bw40_chan165_5g',
        'assoc_mixed_bw40_chan13_2g',
        'assoc_mixed_bw20_chan0_5g',
        'assoc_mixed_ssidspec_2g',
        'assoc_mixed_ssidspec_5g',
        'assoc_mixed_keyspec_2g',
        'assoc_mixed_keyspec_5g',
        'assoc_mixed_ssidchinese_2g',
        'assoc_mixed_ssidchinese_5g',
        'assoc_ssidhide_2g',
        'assoc_ssidhide_5g',
    ],
    'AP_RELAY_BSD',
    [
        'assoc_psk2_near_field_sta',
        'assoc_psk2_near_field_ssidhide',
    ],
    'AP_RELAY_CONFIG_SYNC',
    [
        'assoc_blacklist_sync',
        'assoc_whitelist_sync'
    ]
]


treeInternetAccessApi = [
    'AP_MIXEDPSK_NET_FORBIDDEN',
    [
        'assoc_psk2_netForbidden_2g',
        'assoc_psk2_netForbidden_5g',
        'assoc_psk2_netForbidden_off_2g',
        'assoc_psk2_netForbidden_off_5g'
    ],
    'AP_MIXEDPSK_NET_WHITELIST',
    [
        'assoc_psk2_in_whitelist_5g',
        'assoc_psk2_outof_whitelist_5g',
        'assoc_psk2_in_whitelist_2g',
        'assoc_psk2_outof_whitelist_2g',
    ],
    'AP_MIXEDPSK_NET_BLACKLIST',
    [
        'assoc_psk2_in_blacklist_5g',
        'assoc_psk2_outof_blacklist_5g',
        'assoc_psk2_in_blacklist_2g',
        'assoc_psk2_outof_blacklist_2g',
    ],
    'AP_MIXEDPSK_NET_CUTOFF_LIMITED',
    [
        'assoc_psk2_sta_5g',
        'assoc_psk2_sta_2g',
        'assoc_psk2_sta_ctrloff_5g',
        'assoc_psk2_sta_ctrloff_2g',
    ],
    # 'AP_CLEAR_NET_WHITELIST',
    # [
    #     'assoc_clear_sta_in_whitelist_5g',
    #     'assoc_clear_sta_outof_whitelist_5g',
    #     'assoc_clear_sta_in_whitelist_2g',
    #     'assoc_clear_sta_outof_whitelist_2g',
    # ],
    # 'AP_CLEAR_NET_BLACKLIST',
    # [
    #     'assoc_clear_sta_in_blacklist_5g',
    #     'assoc_clear_sta_outof_blacklist_5g',
    #     'assoc_clear_sta_in_blacklist_2g',
    #     'assoc_clear_sta_outof_blacklist_2g',
    # ],
    # 'AP_CLEAR_NET_CUTOFF_LIMITED',
    # [
    #     'assoc_clear_sta_5g',
    #     'assoc_clear_sta_2g',
    #     'assoc_clear_sta_ctrloff_5g',
    #     'assoc_clear_sta_ctrloff_2g',
    # ],
]


treeAccessControlApi = [
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
    # 'AP_GUEST_CLEAR_WHITELIST',
    # [
    #     'assoc_clear_sta_in_whitelist_guest',
    #     'assoc_clear_sta_outof_whitelist_guest',
    # ],
    #
    # 'AP_GUEST_CLEAR_BLACKLIST',
    # [
    #     'assoc_clear_sta_in_blacklist_guest',
    #     'assoc_clear_sta_outof_blacklist_guest',
    # ],
    'AP_MIXEDPSK_WEB_ACCESS',
    [
        'assoc_psk2_sta_access_web_2g',
        'assoc_psk2_sta_access_web_5g',
    ],

]


treeWirelessRelayApi = [
    'AP_WIRELESS_RELAY_2G',
    [
        'wifiRelay_switchCheck_2g',
        'config_check_5g',
        'config_check_guest',
        'config_check_2g',
        'assoc_afterModeChange_2g',
        'assoc_afterModeChange_5g',
        'assoc_ch36Clr_txMin_5g',
        'assoc_ch52Psk2BW40_txMid_5g',
        'assoc_ch165Mixd_txMax_5g',
        'assoc_ssidSpecHide_2g',
        'assoc_ssidChineseHide_5g'
    ],
]

tree5gWirelessRelayApi = [
    'AP_WIRELESS_RELAY_5G',
    [
        'wifiRelay_switchCheck_5g',
        'config_check_2g',
        'config_check_guest',
        'config_check_5g',
        'assoc_afterModeChange_2g',
        'assoc_afterModeChange_5g',
        'assoc_ch1Clr_txMin_2g',
        'assoc_ch6Psk2BW40_txMid_2g',
        'assoc_ch13keySpec_txMax_2g',
        'assoc_ssidSpecHide_5g',
        'assoc_ssidChineseHide_2g',
    ],
]
treeQosApi = [
    'AP_QOS_MIXEDPSK',
    [
        'assoc_psk2_sta_speedtest_2g',
        # 'assoc_psk_sta_speedtest_2g',
        # 'assoc_tkippsk2_sta_speedtest_2g',
        # 'assoc_tkippsk_sta_speedtest_2g',
        'assoc_psk2_sta_speedtest_5g',
        # 'assoc_psk_sta_speedtest_5g',
        # 'assoc_tkippsk2_sta_speedtest_5g',
        # 'assoc_tkippsk_sta_speedtest_5g',
     ],
    # 'AP_QOS_CLEAR',
    # [
    #     'assoc_clear_sta_speedtest_2g',
    #     'assoc_clear_sta_speedtest_5g',
    # ],
    # 'AP_QOS_PSK2',
    # [
    #     'assoc_psk2_sta_speedtest_2g',
    #     'assoc_psk2_sta_speedtest_5g',
    # ],
    'AP_QOS_GUEST_MIXEDPSK',
    [
        'assoc_psk2_sta_speedtest_guest',
        # 'assoc_psk_sta_speedtest_guest',
        # 'assoc_tkippsk2_sta_speedtest_guest',
        # 'assoc_tkippsk_sta_speedtest_guest',
    ],
    'AP_QOS_ROUTERSELF',
    [
        'routerSelf_speedtest'
    ]
]

treeThroughputDUTApi = [
    "AP_CLEAR_CHAN1_BW20_DUT_THROUGHPUT",
    [
        "assoc_sta_throughput_2g",
    ],
    "AP_CLEAR_CHAN6_BW20_DUT_THROUGHPUT",
    [
        "assoc_sta_throughput_2g",
    ],
    "AP_CLEAR_CHAN11_BW20_DUT_THROUGHPUT",
    [
        "assoc_sta_throughput_2g",
    ],
    "AP_CLEAR_CHAN13_BW20_DUT_THROUGHPUT",
    [
        "assoc_sta_throughput_2g",
    ],
    "AP_CLEAR_CHAN1_BW40_DUT_THROUGHPUT",
    [
        "assoc_sta_throughput_2g",
    ],
    "AP_CLEAR_CHAN6_BW40_DUT_THROUGHPUT",
    [
        "assoc_sta_throughput_2g",
    ],
    "AP_CLEAR_CHAN11_BW40_DUT_THROUGHPUT",
    [
        "assoc_sta_throughput_2g",
    ],
    "AP_CLEAR_CHAN13_BW40_DUT_THROUGHPUT",
    [
        "assoc_sta_throughput_2g",
    ],
    "AP_PSK2_CHAN1_BW20_DUT_THROUGHPUT",
    [
        "assoc_sta_throughput_2g",
    ],
    "AP_PSK2_CHAN6_BW20_DUT_THROUGHPUT",
    [
        "assoc_sta_throughput_2g",
    ],
    "AP_PSK2_CHAN11_BW20_DUT_THROUGHPUT",
    [
        "assoc_sta_throughput_2g",
    ],
    "AP_PSK2_CHAN13_BW20_DUT_THROUGHPUT",
    [
        "assoc_sta_throughput_2g",
    ],
    "AP_PSK2_CHAN1_BW40_DUT_THROUGHPUT",
    [
        "assoc_sta_throughput_2g",
    ],
    "AP_PSK2_CHAN6_BW40_DUT_THROUGHPUT",
    [
        "assoc_sta_throughput_2g",
    ],
    "AP_PSK2_CHAN11_BW40_DUT_THROUGHPUT",
    [
        "assoc_sta_throughput_2g",
    ],
    "AP_PSK2_CHAN13_BW40_DUT_THROUGHPUT",
    [
        "assoc_sta_throughput_2g",
    ],
    "AP_CLEAR_CHAN36_BW20_DUT_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_CLEAR_CHAN52_BW20_DUT_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_CLEAR_CHAN149_BW20_DUT_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_CLEAR_CHAN165_BW20_DUT_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_CLEAR_CHAN36_BW40_DUT_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_CLEAR_CHAN44_BW40_DUT_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_CLEAR_CHAN52_BW40_DUT_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_CLEAR_CHAN60_BW40_DUT_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_CLEAR_CHAN149_BW40_DUT_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_CLEAR_CHAN157_BW40_DUT_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_CLEAR_CHAN36_BW80_DUT_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_CLEAR_CHAN52_BW80_DUT_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_CLEAR_CHAN149_BW80_DUT_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_PSK2_CHAN36_BW20_DUT_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_PSK2_CHAN52_BW20_DUT_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_PSK2_CHAN149_BW20_DUT_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_PSK2_CHAN165_BW20_DUT_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_PSK2_CHAN36_BW40_DUT_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_PSK2_CHAN44_BW40_DUT_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_PSK2_CHAN52_BW40_DUT_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_PSK2_CHAN60_BW40_DUT_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_PSK2_CHAN149_BW40_DUT_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_PSK2_CHAN157_BW40_DUT_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_PSK2_CHAN36_BW80_DUT_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_PSK2_CHAN52_BW80_DUT_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_PSK2_CHAN149_BW80_DUT_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
]

treeThroughputLANApi = [
    "AP_CLEAR_CHAN1_BW20_LAN_THROUGHPUT",
    [
        "assoc_sta_throughput_2g",
    ],
    "AP_CLEAR_CHAN6_BW20_LAN_THROUGHPUT",
    [
        "assoc_sta_throughput_2g",
    ],
    "AP_CLEAR_CHAN11_BW20_LAN_THROUGHPUT",
    [
        "assoc_sta_throughput_2g",
    ],
    "AP_CLEAR_CHAN13_BW20_LAN_THROUGHPUT",
    [
        "assoc_sta_throughput_2g",
    ],
    "AP_CLEAR_CHAN1_BW40_LAN_THROUGHPUT",
    [
        "assoc_sta_throughput_2g",
    ],
    "AP_CLEAR_CHAN6_BW40_LAN_THROUGHPUT",
    [
        "assoc_sta_throughput_2g",
    ],
    "AP_CLEAR_CHAN11_BW40_LAN_THROUGHPUT",
    [
        "assoc_sta_throughput_2g",
    ],
    "AP_CLEAR_CHAN13_BW40_LAN_THROUGHPUT",
    [
        "assoc_sta_throughput_2g",
    ],
    "AP_PSK2_CHAN1_BW20_LAN_THROUGHPUT",
    [
        "assoc_sta_throughput_2g",
    ],
    "AP_PSK2_CHAN6_BW20_LAN_THROUGHPUT",
    [
        "assoc_sta_throughput_2g",
    ],
    "AP_PSK2_CHAN11_BW20_LAN_THROUGHPUT",
    [
        "assoc_sta_throughput_2g",
    ],
    "AP_PSK2_CHAN13_BW20_LAN_THROUGHPUT",
    [
        "assoc_sta_throughput_2g",
    ],
    "AP_PSK2_CHAN1_BW40_LAN_THROUGHPUT",
    [
        "assoc_sta_throughput_2g",
    ],
    "AP_PSK2_CHAN6_BW40_LAN_THROUGHPUT",
    [
        "assoc_sta_throughput_2g",
    ],
    "AP_PSK2_CHAN11_BW40_LAN_THROUGHPUT",
    [
        "assoc_sta_throughput_2g",
    ],
    "AP_PSK2_CHAN13_BW40_LAN_THROUGHPUT",
    [
        "assoc_sta_throughput_2g",
    ],
    "AP_CLEAR_CHAN36_BW20_LAN_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_CLEAR_CHAN52_BW20_LAN_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_CLEAR_CHAN149_BW20_LAN_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_CLEAR_CHAN165_BW20_LAN_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_CLEAR_CHAN36_BW40_LAN_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_CLEAR_CHAN44_BW40_LAN_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_CLEAR_CHAN52_BW40_LAN_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_CLEAR_CHAN60_BW40_LAN_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_CLEAR_CHAN149_BW40_LAN_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_CLEAR_CHAN157_BW40_LAN_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_CLEAR_CHAN36_BW80_LAN_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_CLEAR_CHAN52_BW80_LAN_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_CLEAR_CHAN149_BW80_LAN_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_PSK2_CHAN36_BW20_LAN_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_PSK2_CHAN52_BW20_LAN_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_PSK2_CHAN149_BW20_LAN_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_PSK2_CHAN165_BW20_LAN_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_PSK2_CHAN36_BW40_LAN_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_PSK2_CHAN44_BW40_LAN_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_PSK2_CHAN52_BW40_LAN_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_PSK2_CHAN60_BW40_LAN_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_PSK2_CHAN149_BW40_LAN_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_PSK2_CHAN157_BW40_LAN_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_PSK2_CHAN36_BW80_LAN_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_PSK2_CHAN52_BW80_LAN_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_PSK2_CHAN149_BW80_LAN_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
]


treeThroughputWANApi = [
    "AP_CLEAR_CHAN1_BW20_WAN_THROUGHPUT",
    [
        "assoc_sta_throughput_2g",
    ],
    "AP_CLEAR_CHAN6_BW20_WAN_THROUGHPUT",
    [
        "assoc_sta_throughput_2g",
    ],
    "AP_CLEAR_CHAN11_BW20_WAN_THROUGHPUT",
    [
        "assoc_sta_throughput_2g",
    ],
    "AP_CLEAR_CHAN13_BW20_WAN_THROUGHPUT",
    [
        "assoc_sta_throughput_2g",
    ],
    "AP_CLEAR_CHAN1_BW40_WAN_THROUGHPUT",
    [
        "assoc_sta_throughput_2g",
    ],
    "AP_CLEAR_CHAN6_BW40_WAN_THROUGHPUT",
    [
        "assoc_sta_throughput_2g",
    ],
    "AP_CLEAR_CHAN11_BW40_WAN_THROUGHPUT",
    [
        "assoc_sta_throughput_2g",
    ],
    "AP_CLEAR_CHAN13_BW40_WAN_THROUGHPUT",
    [
        "assoc_sta_throughput_2g",
    ],
    "AP_PSK2_CHAN1_BW20_WAN_THROUGHPUT",
    [
        "assoc_sta_throughput_2g",
    ],
    "AP_PSK2_CHAN6_BW20_WAN_THROUGHPUT",
    [
        "assoc_sta_throughput_2g",
    ],
    "AP_PSK2_CHAN11_BW20_WAN_THROUGHPUT",
    [
        "assoc_sta_throughput_2g",
    ],
    "AP_PSK2_CHAN13_BW20_WAN_THROUGHPUT",
    [
        "assoc_sta_throughput_2g",
    ],
    "AP_PSK2_CHAN1_BW40_WAN_THROUGHPUT",
    [
        "assoc_sta_throughput_2g",
    ],
    "AP_PSK2_CHAN6_BW40_WAN_THROUGHPUT",
    [
        "assoc_sta_throughput_2g",
    ],
    "AP_PSK2_CHAN11_BW40_WAN_THROUGHPUT",
    [
        "assoc_sta_throughput_2g",
    ],
    "AP_PSK2_CHAN13_BW40_WAN_THROUGHPUT",
    [
        "assoc_sta_throughput_2g",
    ],
    "AP_CLEAR_CHAN36_BW20_WAN_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_CLEAR_CHAN52_BW20_WAN_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_CLEAR_CHAN149_BW20_WAN_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_CLEAR_CHAN165_BW20_WAN_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_CLEAR_CHAN36_BW40_WAN_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_CLEAR_CHAN44_BW40_WAN_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_CLEAR_CHAN52_BW40_WAN_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_CLEAR_CHAN60_BW40_WAN_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_CLEAR_CHAN149_BW40_WAN_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_CLEAR_CHAN157_BW40_WAN_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_CLEAR_CHAN36_BW80_WAN_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_CLEAR_CHAN52_BW80_WAN_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_CLEAR_CHAN149_BW80_WAN_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_PSK2_CHAN36_BW20_WAN_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_PSK2_CHAN52_BW20_WAN_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_PSK2_CHAN149_BW20_WAN_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_PSK2_CHAN165_BW20_WAN_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_PSK2_CHAN36_BW40_WAN_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_PSK2_CHAN44_BW40_WAN_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_PSK2_CHAN52_BW40_WAN_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_PSK2_CHAN60_BW40_WAN_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_PSK2_CHAN149_BW40_WAN_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_PSK2_CHAN157_BW40_WAN_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_PSK2_CHAN36_BW80_WAN_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_PSK2_CHAN52_BW80_WAN_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
    "AP_PSK2_CHAN149_BW80_WAN_THROUGHPUT",
    [
        "assoc_sta_throughput_5g",
    ],
]


treeSpeedtestApi = [
    'AP_WAN_BANDWIDTH',
    [
        'test_wan_bandwidth',
    ],
    'AP_PSK2_CHAN11_OOKLA',
    [
        'assoc_psk2_sta_speedtest_2g',
    ],
    'AP_CLEAR_CHAN11_OOKLA',
    [
        'assoc_clear_sta_speedtest_2g',
    ],
    'AP_PSK2_CHAN149_OOKLA',
    [
        'assoc_psk2_sta_speedtest_5g',
    ],
    'AP_CLEAR_CHAN149_OOKLA',
    [
        'assoc_clear_sta_speedtest_5g',
    ],
    'AP_GUEST_PSK2_OOKLA',
    [
        'assoc_psk2_sta_speedtest_guest',
    ],
    'AP_GUEST_CLEAR_OOKLA',
    [
        'assoc_clear_sta_speedtest_guest',
    ],
    'AP_RELAY_PSK2_CHAN11_OOKLA',
    [
        'assoc_psk2_sta_speedtest_2g',
    ],
    'AP_RELAY_CLEAR_CHAN11_OOKLA',
    [
        'assoc_clear_sta_speedtest_2g',
    ],
    'AP_RELAY_PSK2_CHAN149_OOKLA',
    [
        'assoc_psk2_sta_speedtest_5g',
    ],
    'AP_RELAY_CLEAR_CHAN149_OOKLA',
    [
        'assoc_clear_sta_speedtest_5g',
    ],
    'AP_WIRELESS_RELAY_PSK2_CHAN11_OOKLA',
    [
        'assoc_psk2_sta_speedtest_2g',
    ],
    'AP_WIRELESS_RELAY_CLEAR_CHAN11_OOKLA',
    [
        'assoc_clear_sta_speedtest_2g',
    ],
    'AP_WIRELESS_RELAY_PSK2_CHAN149_OOKLA',
    [
        'assoc_psk2_sta_speedtest_5g',
    ],
    'AP_WIRELESS_RELAY_CLEAR_CHAN149_OOKLA',
    [
        'assoc_clear_sta_speedtest_5g',
    ],
]

treeOthersApi = [
    'AP_CHECK',
    [
        'check_ap_reboot_lastestpower',
        'check_ap_upgrade_lastestpower',
        'check_ap_reset_lastestpower',
    ],
    'STA_CHECK',
    [
        'check_sta_after_apReboot'
    ]
]

treeStressApi = [
    "AP_CLEAR_CHAN_REPEAT",
    [
        "assoc_repeat_clear_sta_2g",
        "assoc_repeat_clear_sta_5g"
    ],
    "AP_PSK2_CHAN_REPEAT",
    [
        "assoc_repeat_psk2_sta_2g",
        "assoc_repeat_psk2_sta_5g",
    ],
    "AP_MIXEDPSK_CHAN_REPEAT",
    [
        "assoc_repeat_psk2_sta_2g",
        "assoc_repeat_psk_sta_2g",
        "assoc_repeat_tkippsk2_sta_2g",
        "assoc_repeat_tkippsk_sta_2g",
        "assoc_repeat_psk2_sta_5g",
        "assoc_repeat_psk_sta_5g",
        "assoc_repeat_tkippsk2_sta_5g",
         "assoc_repeat_tkippsk_sta_5g",
    ],
    "AP_GUEST_CLEAR_REPEAT",
    [
        "assoc_repeat_clear_sta_guest",
    ],
    "AP_GUEST_MIXEDPSK_REPEAT",
    [
        "assoc_repeat_psk2_sta_guest",
        "assoc_repeat_psk_sta_guest",
        "assoc_repeat_tkippsk2_sta_guest",
        "assoc_repeat_tkippsk_sta_guest",
    ],
    "AP_GUEST_PSK2_REPEAT",
    [
        "assoc_repeat_psk2_sta_guest",
    ],
]

treeIxChariotApi = [
    "IxChariot_Lan2Wifi_2g_CHAN1_BW20",
    [
        "tx",
        "rx"
    ],
    "IxChariot_Lan2Wifi_2g_CHAN6_BW20",
    [
        "tx",
        "rx"
    ],
    "IxChariot_Lan2Wifi_2g_CHAN11_BW20",
    [
        "tx",
        "rx"
    ],
    "IxChariot_Lan2Wifi_2g_CHAN1_BW40",
    [
        "tx",
        "rx"
    ],
    "IxChariot_Lan2Wifi_2g_CHAN6_BW40",
    [
        "tx",
        "rx"
    ],
    "IxChariot_Lan2Wifi_2g_CHAN11_BW40",
    [
        "tx",
        "rx"
    ],
    "IxChariot_Lan2Wifi_5g_CHAN36_BW80",
    [
        "tx",
        "rx"
    ],
    "IxChariot_Lan2Wifi_5g_CHAN149_BW80",
    [
        "tx",
        "rx"
    ],
    "IxChariot_Wan2Wifi_2g_CHAN1_BW20",
    [
        "tx",
        "rx"
    ],
    "IxChariot_Wan2Wifi_2g_CHAN6_BW20",
    [
        "tx",
        "rx"
    ],
    "IxChariot_Wan2Wifi_2g_CHAN11_BW20",
    [
        "tx",
        "rx"
    ],
    "IxChariot_Wan2Wifi_2g_CHAN1_BW40",
    [
        "tx",
        "rx"
    ],
    "IxChariot_Wan2Wifi_2g_CHAN6_BW40",
    [
        "tx",
        "rx"
    ],
    "IxChariot_Wan2Wifi_2g_CHAN11_BW40",
    [
        "tx",
        "rx"
    ],
    "IxChariot_Wan2Wifi_5g_CHAN36_BW80",
    [
        "tx",
        "rx"
    ],
    "IxChariot_Wan2Wifi_5g_CHAN149_BW80",
    [
        "tx",
        "rx"
    ]
]
# -------------------------------------------------------

txPower2G = {
    "R1D": [19.75, 23.25, 27],
    "R2D": [19.75, 23.25, 27],
    "R1CM": [13, 15, 16],
    "R3": [13, 15, 16],
    "R1CL": [14, 16, 17],
    "R3L": [14, 16, 17],
    "R3P": [17, 19, 20],
    "R3D": [25, 27, 28],
    "R3A": [14, 16, 17],
    "R3G": [16, 18, 19]
}

txPower5GL = {
    "R1D": [15.5, 18.25, 21],
    "R2D": [15.5, 18.25, 21],
    "R1CM": [13, 15, 16],
    "R3": [13, 15, 16],
    "R3P": [17, 19, 20],
    "R3D": [23, 25, 26],
    "R3A": [13, 15, 16],
    "R3G": [13, 15, 16]
}

txPower5GH = {
    "R1D": [16.25, 19, 22],
    "R2D": [16.25, 19, 22],
    "R1CM": [13, 15, 16],
    "R3": [13, 15, 16],
    "R3P": [17, 19, 20],
    "R3D": [23, 25, 26],
    "R3A": [13, 15, 16],
    "R3G": [13, 15, 16]
}



