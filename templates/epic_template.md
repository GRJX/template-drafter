{{ title }}

Labels: {{ label }}

||Use Case (naam)||Actor||Korte omschrijving (gewenste functionaliteit)||Menu-item||
|{{ use_case }}|{{ actor }}|{{ functional_description }}|{{ menu }}
 
h3. Samenvatting
h4. Korte omschrijving
{{ description }}

h4. Actor
{{ actor }} 

h3. Precondities
{{ pre_conditions }}

h3. Flows
h4. Basic Flow (BF) of Events
*BF1: {{ bf_flow }}*
||Step||Omschrijving||
{{ bf_table_rows }}

h4. Alternative Flows (AF)
*AF1: {{ af_flow }}*
||Step||Omschrijving||
{{ af_table_rows }}

h3. Resultaat
h4. Succescondities
{{ success_conditions }}

h4. Faalcondities
{{ fail_conditions }}

h3. Controles en regels
||Referentie systeemregels||Omschrijving||
{{ business_rules_rows }}

h3. Aanvullende eisen
h4. Voorwaarden
{{ voorwaarden }}

h4. Logische interfaces (naar andere applicaties)
{{ interfaces }}

h3. Logische omschrijving
h4. Input- en outputdocumenten
{{ documents }}
