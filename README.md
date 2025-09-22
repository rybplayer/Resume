# Ryan Batubara's Resume

My data-driven resume in LaTeX. The resume template is [Jake's Resume](https://github.com/jakegut/resume), by [Jake Gutierrez](https://jakegut.com/). The parsers are mine. 

## 🔖 Why?

I wanted a single "source of truth" for my pdf resume and website. I could have written a LaTeX parser, but `.tex` is generally not a good way to store data. Thus, I put the data in Astro-header-like makrdown `.md` documents, so both my LaTeX resume and website can read from the same data source.

## 🛠️ How to use

> I have no idea why anyone but myself would want to build this resume from source.

1. Install the python packages. Make a venv if you want.
2. Run `python3 build_resume.py`.

That's it. Running `parse_data.py` prints the LaTeX output sections.

## 📁 Structure

```
/Users/ryanbatubara/Desktop/#Resume/
├── resume-data/            # Markdown data
│   ├── education/
│   ├── experience/
│   ├── projects/
│   ├── skills/
│   └── achievements/
├── template/               # Stores template
│   └── resume_template.tex
├── parse_data.py           # Markdown to LaTeX
├── build_resume.py         # Build Script
└── RyanBatubaraResume.tex  # Final tex
└── RyanBatubaraResume.pdf  # Final pdf
```

## ✏️ Adding New Content

#### 1. Education
Create a new `.md` file in `data/education/`:

```markdown
---
institution: 'University Name'
location: 'City, State'
degree: 'Your Degree'
startDate: 'Start Date'
endDate: 'End Date'
coursework: 'Relevant coursework (optional)'
---
```

#### 2. Experience
Create a new `.md` file in `data/experience/`:

```markdown
---
title: 'Job Title'
company: 'Company Name'
location: 'City, State'
startDate: 'Start Date'
endDate: 'End Date'
link: 'https://company-website.com' # optional
accomplishments:
  - 'Achievement 1'
  - 'Achievement 2'
paperLink: 'https://paper-url.com' # optional, for linking "this paper"
---
```

#### 3. Projects
Create a new `.md` file in `data/projects/`:

```markdown
---
name: 'Project Name'
technologies: 'Tech1, Tech2, Tech3'
link: 'https://project-link.com'
accomplishments:
  - 'What you built/achieved'
  - 'Impact or results'
---
```

#### 4. Skills
Create a new `.md` file in `data/skills/`:

```markdown
---
category: 'Category Name'
skills: 'Skill1, Skill2, Skill3, Skill4'
---
```

#### 5. Achievements
Create a new `.md` file in `data/achievements/`:

```markdown
---
title: 'Achievement Title'
location: 'Location (optional)'
year: 'Year'
link: 'https://verification-link.com'
---
```

## 📝 Data Format Notes

- All strings should be quoted with single quotes `'text'`
- Lists use YAML format with `- 'item'` syntax
- Links are automatically formatted as LaTeX hyperlinks
- Special characters in URLs (like underscores) are automatically escaped
- The `_template.md` files show the expected format for each section