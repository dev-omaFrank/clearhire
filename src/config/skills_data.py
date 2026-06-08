# Skills dictionary, grouped by domain.
#
# Clearhire ships configured for tech roles, but the engine is domain-agnostic:
# to screen for a different field (e.g. a non-tech company), add a domain to
# SKILL_DOMAINS and list it in ACTIVE_DOMAINS. Nothing else needs to change.
#
# Note on naming: skills use unambiguous, whole-word forms to avoid false
# positives during matching (e.g. "golang" not "go", "c programming" not "c",
# "r programming" not "r"), since the matcher uses word-boundary matching.

SKILL_DOMAINS = {
    "software_engineering": [
        "python", "java", "c programming", "c plus plus", "c sharp", "golang",
        "rust", "kotlin", "scala", "ruby", "php", "object oriented programming",
        "data structures", "algorithms", "git", "github", "gitlab",
        "rest api", "graphql", "microservices", "design patterns",
        "unit testing", "integration testing", "agile", "scrum",
    ],

    "web_development": [
        "javascript", "typescript", "html", "css", "sass", "tailwind",
        "react", "next.js", "vue", "angular", "svelte", "node.js", "express",
        "django", "flask", "fastapi", "spring boot", "laravel",
        "redux", "webpack", "vite", "responsive design", "web accessibility",
    ],

    "data_ai": [
        "sql", "postgresql", "mysql", "mongodb", "pandas", "numpy",
        "machine learning", "deep learning", "natural language processing",
        "computer vision", "tensorflow", "pytorch", "scikit-learn",
        "data analysis", "data visualization", "power bi", "tableau",
        "etl", "data pipelines", "apache spark", "jupyter",
    ],

    "cloud_devops": [
        "aws", "azure", "google cloud", "docker", "kubernetes", "terraform",
        "ansible", "jenkins", "github actions", "ci/cd", "linux",
        "bash scripting", "nginx", "prometheus", "grafana",
        "infrastructure as code", "serverless", "load balancing",
    ],

    # ── Defined but inactive: examples of extending Clearhire to new fields. ──
    # Add the name to ACTIVE_DOMAINS to switch any of these on.

    "mobile_development": [
        "swift", "objective c", "android", "ios", "flutter", "dart",
        "react native", "jetpack compose", "swiftui", "xcode", "gradle",
    ],

    "cybersecurity": [
        "penetration testing", "vulnerability assessment", "siem", "firewalls",
        "encryption", "incident response", "threat modeling", "owasp",
        "network security", "identity and access management",
    ],

    # Non-tech example, kept to prove the engine is not tech-specific.
    "banking": [
        "cash handling", "account management", "anti money laundering",
        "know your customer", "bank secrecy act", "wire transfer",
        "loan processing", "regulatory compliance", "risk assessment",
    ],
}

# Shared across every domain.
SOFT_SKILLS = [
    "communication", "leadership", "teamwork", "problem solving",
    "critical thinking", "time management", "adaptability", "creativity",
    "collaboration", "attention to detail", "organization", "multitasking",
    "mentoring", "stakeholder management",
]

# Which domains this deployment screens for. Edit this list to reconfigure.
ACTIVE_DOMAINS = [
    "software_engineering",
    "web_development",
    "data_ai",
    "cloud_devops",
]

# Flattened, de-duplicated list the matcher consumes. Kept as ALL_SKILLS for
# backwards compatibility with src/core/skills.py.
ALL_SKILLS = list(dict.fromkeys(
    [skill for domain in ACTIVE_DOMAINS for skill in SKILL_DOMAINS[domain]]
    + SOFT_SKILLS
))
