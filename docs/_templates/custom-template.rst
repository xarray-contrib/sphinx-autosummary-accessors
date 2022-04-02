{{ fullname }}
{{ underline }}

.. autoclass:: {{ [module, objname] | join('.') }}

   {% block methods %}
   .. automethod:: __init__

   {% if methods %}
   .. rubric:: {{ _('Methods') }}

   .. autosummary::
      :toctree: generated/
   {% for item in methods %}
      {% if item != "__init__" %}
         ~{{ [module, name] | join('.') }}.{{ item }}
      {% endif %}
   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block attributes %}
   {% if attributes %}
   .. rubric:: {{ _('Attributes') }}

   .. autosummary::
      :toctree: generated/
   {% for item in attributes %}
      ~{{ [module, name] | join('.') }}.{{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}
