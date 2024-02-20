
filebeat_yaml_template = """filebeat.inputs:{% for index, row in data.iterrows() %}{%- if index >= 0 %}  {# Adjusted the condition to start from the 4th row of the Excel file #}
- type: httpjson
  enabled: true
  id: {{ row['id'] }}
  interval: {{ row['interval'] }}
  request.url: {% for url in row['request url'].split(', ') %}
    "{{ url.strip() }}"{% if not loop.last %},{% endif %}{% endfor %}
  auth.basic.user: "{{ row['username'] }}"
  auth.basic.password: "{{ row['password'] }}"
  request.method: "{{ row['request method'] }}"
  request.transforms:
      {% for i in range(row['target'].split(', ')|length) %}
      - set:
          target: {{ row['target'].split(', ')[i] }}
          value: "{{ row['value'].split(', ')[i] }}"
      {% endfor %}



  response.decode_as: application/json
  response.split:
    target: body.metricValues
    type: array
    keep_parent: true

  processors:
    - decode_json_fields:
        fields: ["message"]
        target: "json"
        process_array: true
        max_depth: 1
        target: ""
        overwrite_keys: false
        add_error_key: true

    - add_fields:
        target: system_info
        fields:
          service_id: '{{ row['service_id'] }}'
          monitoring_type: '{{ row['monitoring_type'] }}'
          Service_Name: '{{ row['service_name'] }}'
          service_offering_1: '{{ row['service_offering_1'] }}'
          Application_Name: '{{ row['application_name'] }}'
          service_offering_2: '{{ row['service_offering_2'] }}'
          Platform: '{{ row['platform'] }}'
          Tribe: '{{ row['tribe'] }}'
          Partner_id: '{{ row['partner_id'] }}'

    - dissect:
        tokenizer: "{{ row['tokenizer'] }}"
        field: "{{ row['field'] }}"
        target_prefix: "{{ row['target prefix'] }}"
{%- endif %}
{% endfor %}
"""

