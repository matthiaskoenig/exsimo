[Experiments](index.html)

# {{ exp_id }}

## Model
* **SBML**: [{{ model_path }}]({{ model_path }})
* **HTML**: [{{ report_path }}]({{ report_path }})

## Datasets
{% for dset_id in datasets %}
* [{{ dset_id }}.tsv](./sbmlsim/{{ exp_id }}_data_{{ dset_id }}.tsv)
{% endfor %}

## Figures
{% for fig_id in figures %}
* [{{ exp_id }}_{{ fig_id }}.png]({{ exp_id }}_{{ fig_id }}.png) ([SVG]({{ exp_id }}_{{ fig_id }}.svg))
{% endfor %}

{% for fig_id in figures %}
### {{ fig_id }}
![{{ exp_id }}_{{ fig_id }}.svg]({{ exp_id }}_{{ fig_id }}.svg)
{% endfor %}


## Code
[{{ code_path }}]({{ code_path }})

```python
{{ code }}
```