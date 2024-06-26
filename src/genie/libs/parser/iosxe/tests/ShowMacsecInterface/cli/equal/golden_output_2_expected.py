expected_output = {
    "macsec-data": {
        "status": "enabled",
        "replay-protect-status": "enabled",
        "replay-window": "4294967295",
        "include-sci": "yes",
        "use-es-enable": "no",
        "use-scb-enable": "no",
        "admin-pt2pt-mac": "forceTrue(1)",
        "pt2pt-mac-operational": "no",
        "cipher": "GCM-AES-XPN-256",
        "confidentiality-offset": "0",
    },
    "capabilities": {
        "icv-length": "16",
        "data-length-change-supported": "yes",
        "max-rx-sa": "16",
        "max-tx-sa": "16",
        "max-rx-sc": "8",
        "max-tx-sc": "8",
        "validate-frames": "strict",
        "pn-threshold-notification-support": "Yes",
        "ciphers-supported": [
            "GCM-AES-128",
            "GCM-AES-256",
            "GCM-AES-XPN-128",
            "GCM-AES-XPN-256",
        ],
    },
    "access-control": "must secure",
    "cleartag-details": {"type": "one dot1q in clear", "vlanid1": "111"},
    "transmit-secure-channels": {
        "sci": "F87A412527020488",
        "sc-state": "inUse(1)",
        "elapsed-time": "7w0d",
        "start-time": "7w0d",
        "current-an": "0",
        "previous-an": "-",
        "next-pn": "250",
        "sa-state": "inUse(1)",
        "confidentiality": "yes",
        "sak-unchanged": "yes",
        "sa-create-time": "01:09:26",
        "sa-start-time": "7w0d",
        "sc-statistics": {
            "auth-only-pkts": "0",
            "auth-only-bytes": "0",
            "encrypted-pkts": "0",
            "encrypted-bytes": "0",
        },
        "sa-statistics": {
            "auth-only-pkts": "0",
            "auth-only-bytes": "0",
            "encrypted-pkts": "244",
            "encrypted-bytes": "24876",
        },
        "port-statistics": {"egress-untag-pkts": "0", "egress-long-pkts": "0"},
    },
    "receive-secure-channels": {
        "6CB2AE4A5F050451": {
            "sc-state": "inUse(1)",
            "elapsed-time": "7w0d",
            "start-time": "7w0d",
            "current-an": "0",
            "previous-an": "-",
            "next-pn": "30",
            "rx-sa-count": "0",
            "sa-state": "inUse(1)",
            "sak-unchanged": "yes",
            "sa-create-time": "01:09:24",
            "sa-start-time": "7w0d",
            "sc-statistics": {
                "notvalid-pkts": "0",
                "invalid-pkts": "0",
                "valid-pkts": "0",
                "late-pkts": "0",
                "uncheck-pkts": "0",
                "delay-pkts": "0",
                "unusedsa-pkts": "0",
                "nousingsa-pkts": "0",
                "validated-bytes": "0",
                "decrypted-bytes": "0",
            },
            "sa-statistics": {
                "notvalid-pkts": "0",
                "invalid-pkts": "0",
                "valid-pkts": "19",
                "unusedsa-pkts": "0",
                "nousingsa-pkts": "0",
                "validated-bytes": "0",
                "decrypted-bytes": "1862",
            },
        },
        "ECCE1346F9020488": {
            "sc-state": "inUse(1)",
            "elapsed-time": "7w0d",
            "start-time": "7w0d",
            "current-an": "0",
            "previous-an": "-",
            "next-pn": "250",
            "rx-sa-count": "0",
            "sa-state": "inUse(1)",
            "sak-unchanged": "yes",
            "sa-create-time": "01:09:24",
            "sa-start-time": "7w0d",
            "sc-statistics": {
                "notvalid-pkts": "0",
                "invalid-pkts": "0",
                "valid-pkts": "0",
                "late-pkts": "0",
                "uncheck-pkts": "0",
                "delay-pkts": "0",
                "unusedsa-pkts": "0",
                "nousingsa-pkts": "0",
                "validated-bytes": "0",
                "decrypted-bytes": "0",
            },
            "sa-statistics": {
                "notvalid-pkts": "0",
                "invalid-pkts": "0",
                "valid-pkts": "231",
                "unusedsa-pkts": "0",
                "nousingsa-pkts": "0",
                "validated-bytes": "0",
                "decrypted-bytes": "23522",
            },
        },
        "port-statistics": {
            "ingress-untag-pkts": "0",
            "ingress-notag-pkts": "28",
            "ingress-badtag-pkts": "0",
            "ingress-unknownsci-pkts": "0",
            "ingress-nosci-pkts": "0",
            "ingress-overrun-pkts": "0",
        },
    },
}
