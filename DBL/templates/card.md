## Description

{{ opp.description }}

## Requirements

{% for requirement in opp.requirements %}
* {{ requirement }}
{% endfor %}

{% if 'selection_stages' in opp %}

## Selection Stages

{% for ss in opp.selection_stages %}
1. {{ ss.name }} ({{ss.period}})
{% for ss_obj in ss.objectives %}
    * {{ss_obj}}
{% endfor %}
{% endfor %}

{% endif %}

## Additional Information


### Target audience
{% if 'target' not in opp %}No info provided{% else %}
{% for target in opp.target %}
* {{ target }}
{% endfor %}
{% endif %}
### Field
{% if 'discipline' not in opp %}No info provided{% else %}
{% for dis in opp.discipline %}
* {{ dis }}
{% endfor %}
{% endif %}
### Advantages
{% if 'advantages' not in opp %}No info provided{% else %}
{% for adv in opp.advantages %}
* {{ adv }}
{% endfor %}
{% endif %}

{% for adt in opp.additional %}
### {{adt.title}}
{{adt.description}}
{% endfor %}

### Other
{% if 'period_of_internship' in opp %}
* Duration: {{opp.period_of_internship}}
{% endif %}
{% if 'allowance' in opp %}
* Allowance: {{opp.allowance}}
{% endif %}
{% if 'expenses' in opp %}
* Expenses: {{opp.expenses}}
{% endif %}
