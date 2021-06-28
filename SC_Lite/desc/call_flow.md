---
title : "Сценарии работы"
description : ""
weight : 6
---

## Сценарий обработки исходящих SMS с BRT–тарификацией

{{<mermaid>}}
sequenceDiagram
  participant M as MSC
  participant SL as SC_Lite
  participant S as SMSC
  participant U as UBS
autonumber
  M ->> SL: MAP-FSM
  SL ->> U: smpp_auth_sms
  U ->> SL: smpp_auth_sms_resp
  SL ->> S: smpp_data_sm
  S ->> SL: SMPP_data_sm_resp
  SL ->> M: MAP-FSM_Resp
  SL ->> U: smpp_end_sms
  U ->> SL: smpp_end_sms_ACK
{{</mermaid>}}

## Сценарий обмена SMS–сообщениями

{{<mermaid>}}
sequenceDiagram
  participant M as MSC
  participant SL as SC_Lite
  participant S as SMSC
autonumber
  S ->> SL: smpp_bind_transmitter_resp (system_id; password; system_type)
  SL ->> S: smpp_bind_transmitter_resp (system_id)
  S ->> SL: smpp_data_sm (serv.type=00; dest_addr=MSISDN<br/>esm_class=xx000010; registered_delivery=01)
  SL ->> M: MAP-SRI-SM
  M ->> SL: MAP-SRI-SM_Resp
  SL ->> M: MAP-FSM (MSISDN-destination<br/>MSISDN-originating)
  M ->> SL: MAP-FSM_Resp
  SL ->> S: smpp_data_sm_resp
  M ->> SL: MAP-FSM (MSISDN-destination<br/>MSISDN-originating)
  SL ->> S: smpp_data_sm (serv.type=00; dest_addr=MSISDN<br/>esm_class=00; registered_delivery=00)
  S ->> SL: smpp_data_sm_resp
  SL ->> M: MAP-FSM_Resp
{{</mermaid>}}

## Сценарий MT‒SMS с Diameter–тарификацией

{{<mermaid>}}
sequenceDiagram
  participant M as MSC
  participant SL as SC_Lite
  participant H as HLR
  participant O as OCS
  participant S as SMSC
autonumber
  S ->> SL: smpp_data_sm
  SL ->> O: Diameter CCR-Initial
  O ->> SL: Diameter CCA-Initial (Result-Code MSCC: Result-Code)
  SL ->> H: MAP-SRI-SM (MSISDN)
  H ->> SL: MAP-SRI-SM_Resp (MSISDN)
  SL ->> M: MAP-MT-FSM
  M ->> SL: MAP-MT-FSM_Resp
  SL -->> O: Diameter CCR-Termination
  O -->> SL: Diameter CCA-Termination (Result-Code MSCC: Result-Code)
  SL -->> S: smpp_data_sm_resp
{{</mermaid>}}

## Сценарий MO‒SMSс Diameter–тарификацией

{{<mermaid>}}
sequenceDiagram
  participant M as MSC
  participant SL as SC_Lite
  participant S as SMSC
  participant O as OCS
autonumber
  M ->> SL: MAP-MO-FSM
  SL ->> O: Diameter CCR-Initial
  O ->> SL: Diameter CCA-Initial (Result-Code MSCC: Result-Code)
  SL ->> S: smpp_data_sm
  S -->> SL: smpp_data_sm_resp
  SL ->> M: MAP-MO-FSM_Resp
  SL ->> O: Diameter CCR-Termination
  O ->> SL: Diameter CCA-Termination (Result-Code MSCC: Result-Code)
{{</mermaid>}}

## Сценарий MO‒USSD Phase 1

{{<mermaid>}}
sequenceDiagram
  participant M as MSC
  participant SL as SC_Lite
  participant E as ESME
autonumber
  M ->> SL: MAP–PSSD (IMSI–m; MSISDN–o<br/>data_coding–m; USSD_string–m)
  SL ->> E: smpp_deliver_sm (serv.type=USSD; ussd_serv_op=PSSDind<br/>source_addr=MSISDN/IMSI; short_message)
  E ->> SL: smpp_deliver_sm_resp
  E ->> SL: smpp_submit_sm (serv.type=USSD; ussd_serv_op=PSSDresp<br/>dest_addr=MSISDN/IMSI; short_message)
  SL ->> M: MAP–PSSD_Resp (data_coding; USSD_string)
  SL ->> E: smpp_submit_sm_resp
{{</mermaid>}}

## Сценарий MO‒USSD Phase 2

{{<mermaid>}}
sequenceDiagram
  participant M as MSC
  participant SL as SC_Lite
  participant E as ESME
autonumber
  M ->> SL: MAP–PSSR (IMSI–m; MSISDN–o;<br/>data_coding–m; USSD_string–m)
  SL ->> E: smpp_deliver_sm (serv.type=USSD; ussd_serv_op=PSSRind<br/>source_addr=MSISDN/IMSI; short_message)
  E ->> SL: smpp_deliver_sm_resp
  E ->> SL: smpp_submit_sm (serv.type=USSD; ussd_serv_op=PSSDresp<br/>dest_addr=MSISDN/IMSI; short_message)
  SL ->> M: MAP–USSR (data_coding; USSD_string)
  SL ->> E: smpp_submit_sm_resp
  M ->> SL: MAP–USSR_Resp (data_coding; USSD_string)
  SL -->> E: smpp_deliver_sm (serv.type=USSD; ussd_serv_op=USSRconf<br/>ource_addr=MSISDN/IMSI; short_message)
  E ->> SL: smpp_deliver_sm_resp
  E ->> SL: smpp_submit_sm (serv.type=USSD; ussd_serv_op=PSSR_resp<br/>source_addr=MSISDN/IMSI; short_message)
  SL ->> M: MAP–PSSR_Resp (IMSI–m; data_coding–o; USSD_string–o)
  SL ->> E: smpp_submit_sm_resp
{{</mermaid>}}
 
## Сценарий MT‒USSD Phase 2

{{<mermaid>}}
sequenceDiagram
  participant M as MSC
  participant SL as SC_Lite
  participant E as ESME
autonumber
  E ->> SL: smpp_submit_sm (serv.type=USSD; ussd_serv_op=USSN<br/>dest_addr=MSISDN/IMSI; short_message)
  SL ->> M: MAP–USSN (IMSI; data_coding; USSD_string)
  SL ->> E: smpp_submit_sm_resp
  M ->> SL: MAP–USSN_Resp (data_coding; USSD_string)
  SL ->> E: SMPP_deliver_sm (serv.type=USSD; ussd_serv_op=USSNconf<br/>source_addr=MSISDN/IMSI; short_message)
  E ->> SL: smpp_deliver_sm_resp
  E ->> SL: smpp_submit_sm (serv.type=USSD; ussd_serv_op=PSSR_resp<br/>source_addr=MSISDN/IMSI; short_message)
  SL ->> M: MAP_RELEASE (TCAP_END)
  SL ->> E: smpp_submit_sm_resp
{{</mermaid>}}


## Сценарий HomeRouting с Diameter–тарификацией

{{<mermaid>}}
sequenceDiagram
  participant S as SMSC
  participant SL as SC_Lite
  participant H as HLR
  participant O as OCS
  participant M as MSC
autonumber
  S ->> SL: MAP–SRI (MSISDN)
  SL ->> S: MAP–SRI_Resp (fake IMSI; GT_VLR=GT_SCL)
  S ->> SL: MAP–MT–FSM
  SL ->> O: Diameter CCR–Initial
  O ->> SL: Diameter CCA-Initial
  loop smpp_data_sm
  SL ->> H: MAP–SRI–SM
  H ->> SL: MAP–SRI–SM_Resp (IMSI; GT_MSC)
  SL ->> M: MAP–MT–FSM
  M ->> SL: MAP–MT–FSM_Resp
  loop smpp_data_sm_resp
  SL ->> O: Diameter CCR–Termination
  O ->> SL: Diameter CCA–Termination
  SL ->> S: MAP–MT–FSM_Resp
{{</mermaid>}}


## Сценарий HR‒SMS на виртуальный номер

{{<mermaid>}}
sequenceDiagram
  participant S as SMSC
  participant SL as SC_Lite
  participant I as IN
  participant M as MSC
autonumber
  S ->> SL: MAP–SRI–FSM (MSISDN; src_real; dest_virt)
  SL ->> S: MAP–SRI–FSM_Resp (fake IMSI; GT_VLR=GT_SCL)
  S ->> SL: MAP–MT–FSM (fake IMSI)
  SL ->> I: HTTP GET vnumber (src_real; dest_virt; dcs)
  I ->> SL: HTTP Response (src_virt; dest_real; footer)
  SL ->> M: smpp_data_sm (src_virt; dest_real; footer)
  M ->> SL: smpp_data_sm_resp
  SL ->> S: MAP–MT–FSM_ACK
{{</mermaid>}}

### HTTP Request:
```xml
<request>
  <src>#addr;#ton;#npi</src>
  <dst>#addr;#ton;#npi</dst>
  <dcs>#dcs</dcs>
  <type>#msgSubType</type>
</request>
```

### HTTP Response:
```xml
<response>
  <src>#Addr;#Ton;#Npi</src>
  <dst>#Addr;#Ton;#Npi</dst>
  <footer>#footer</footer>
  <status>#status</status>
</response>
```

### Параметры запроса и ответа:
* src - параметры отправителя:
  * addr - адрес отправителя;
  * ton - тип номера отправителя;
  * npi - индикатор плана нумерации отправителя.
* dst - параметры получателя:
  * addr - адрес получателя;
  * ton - тип номера получателя;
  * npi - индикатор плана нумерации получателя.
* dcs - схема кодирования;
* footer - футер сообщения;
* status - статус номера;
* type - Вид сообщения.
  * MT - входящие SMS;
  * MO - исходящие SMS;
  * HR - home routing SMS.

### Сценарий MO‒SMS между виртуальными номерами с Diameter–тарификацией

{{<mermaid>}}
sequenceDiagram
  participant S as SMSC
  participant SL as SC_Lite
  participant O as OCS  
  participant I as IN
  participant M as MSC
autonumber
  M ->> SL: MAP–MO–FSM (src_real; dest_virt)
  SL ->> O: Diameter CCR–Initial (src_real; dest_virt)
  O ->> SL: Diameter CCA-Initial
  SL ->> I: HTTP GET vnumber (src_real; dest_virt; dcs)
  I ->> SL: HTTP Response (src_virt; dest_real; footer)
  SL ->> S: smpp_data_sm (src_virt; dest_real; footer)
  S ->> SL: smpp_data_sm_resp
  SL ->> O: Diameter CCR–Termination (src_virt; dest_real)
  O ->> SL: Diameter CCA–Termination
  SL ->> M: MAP–MO–FSM_ACK
{{</mermaid>}}
