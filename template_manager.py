def create_css_templates(css_framework, project_name):
    """Create templates based on the selected CSS framework"""
    try:
        if css_framework == "Bootstrap":
            print("Setting up Bootstrap...")
            with open('static/css/style.css', 'w') as f:
                f.write("""/* Bootstrap CSS */
body {
    font-family: Arial, sans-serif;
}
""")
            with open('templates/index.html', 'w', encoding="utf-8") as f:
                f.write("""{% extends "base.html" %}
{% block content %}
    <div class="container">
        <h1>FlaskForge Project Setup Successful! 🚀</h1>
    </div>
{% endblock %}
{% block css %}

{% endblock %}
{% block js %}

{% endblock %}
""")
            with open('templates/base.html', 'w') as f:
                f.write(f"""<!DOCTYPE html>
<html>
<head>
    <title>{project_name}</title>
    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="/static/css/style.css">
    {{% block css %}}{{% endblock %}}
</head>
<body>
    {{% block content %}}{{% endblock %}}
    {{% block js %}}{{% endblock %}}
</body>
</html>
""")

        elif css_framework == "Tailwind":
            print("Setting up Tailwind CSS...")
            with open('static/css/style.css', 'w') as f:
                f.write("""/* Tailwind CSS */
@tailwind base;
@tailwind components;
@tailwind utilities;
""")
            with open('templates/index.html', 'w', encoding="utf-8") as f:
                f.write("""{% extends "base.html" %}
{% block content %}
    <div class="container mx-auto">
        <h1>FlaskForge Project Setup Successful! 🚀</h1>
    </div>
{% endblock %}
{% block css %}

{% endblock %}
{% block js %}

{% endblock %}
""")
            with open('templates/base.html', 'w') as f:
                f.write(f"""<!DOCTYPE html>
<html>
<head>
    <title>{project_name}</title>
    <!-- Tailwind CSS -->
    <link href="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4" rel="stylesheet">
    <link rel="stylesheet" href="/static/css/style.css">
    {{% block css %}}{{% endblock %}}
</head>
<body>
    {{% block content %}}{{% endblock %}}
    {{% block js %}}{{% endblock %}}
</body>
</html>
""")

        elif css_framework == "None":
            print("No CSS framework selected.")
            with open('templates/index.html', 'w', encoding="utf-8") as f:
                f.write("""{% extends "base.html" %}
{% block content %}
    <h1>FlaskForge Project Setup Successful! 🚀</h1>
{% endblock %}
{% block css %}

{% endblock %}
{% block js %}

{% endblock %}
""")
            with open('templates/base.html', 'w') as f:
                f.write(f"""<!DOCTYPE html>
<html>
<head>
    <title>{project_name}</title>
    <link rel="stylesheet" href="/static/css/style.css">
    {{% block css %}}{{% endblock %}}
</head>
<body>
    {{% block content %}}{{% endblock %}}
    {{% block js %}}{{% endblock %}}
</body>
</html>
""")
        return True
    except OSError as e:
        print(f"Failed to create templates: {e}")
        return False