#!/usr/bin/env python3

import os
import glob
from pathlib import Path

def parse_frontmatter(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if not content.startswith('---'):
        return None
    
    try:
        parts = content.split('---', 2)
        if len(parts) < 3:
            return None
        
        # Simple YAML parser for our specific format
        frontmatter = {}
        yaml_content = parts[1].strip()
        current_list_key = None
        
        for line in yaml_content.split('\n'):
            original_line = line
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            if ':' in line and not line.startswith('  -'):
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                
                # Handle quoted strings
                if value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]
                elif value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                
                # Handle lists that start on next line
                if value == '' and key in ['accomplishments', 'skills']:
                    frontmatter[key] = []
                    current_list_key = key
                    continue
                        
                frontmatter[key] = value
                current_list_key = None
            elif original_line.startswith('  - '):
                # Handle list items
                if current_list_key and current_list_key in frontmatter:
                    item = original_line[4:].strip()
                    if item.startswith("'") and item.endswith("'"):
                        item = item[1:-1]
                    elif item.startswith('"') and item.endswith('"'):
                        item = item[1:-1]
                    frontmatter[current_list_key].append(item)
        
        return frontmatter
    except Exception:
        return None

def generate_education_latex(data_dir):
    education_files = glob.glob(os.path.join(data_dir, 'education', '*.md'))
    education_files = [f for f in education_files if not f.endswith('_template.md')]
    
    latex_content = []
    for file_path in sorted(education_files):
        data = parse_frontmatter(file_path)
        if data:
            latex_content.append(f"    \\resumeSubheading")
            latex_content.append(f"      {{{data['institution']}}}{{{data['location']}}}")
            latex_content.append(f"      {{{data['degree']}}}{{{data['startDate']} -- {data['endDate']}}}")
            if 'coursework' in data and data['coursework']:
                latex_content.append(f"      \\resumeItemListStart")
                latex_content.append(f"        \\resumeItem{{Coursework: {data['coursework']}}}")
                latex_content.append(f"      \\resumeItemListEnd")
    
    return '\n'.join(latex_content)

def generate_experience_latex(data_dir):
    experience_files = glob.glob(os.path.join(data_dir, 'experience', '*.md'))
    experience_files = [f for f in experience_files if not f.endswith('_template.md')]
    
    latex_content = []
    for file_path in sorted(experience_files, reverse=True):
        data = parse_frontmatter(file_path)
        if data:
            latex_content.append(f"    \\resumeSubheading")
            if data.get('link'):
                latex_content.append(f"      {{{data['title']}}}{{{data['startDate']} -- {data['endDate']}}}")
                latex_content.append(f"      {{\\href{{{data['link']}}}{{{data['link']}}}}}{{{data['location']}}}")
            else:
                latex_content.append(f"      {{{data['title']}}}{{{data['startDate']} -- {data['endDate']}}}")
                latex_content.append(f"      {{{data['company']}}}{{{data['location']}}}")
            
            if 'accomplishments' in data and data['accomplishments']:
                latex_content.append(f"      \\resumeItemListStart")
                for accomplishment in data['accomplishments']:
                    if 'paperLink' in data and 'this paper' in accomplishment:
                        accomplishment = accomplishment.replace('this paper', f"\\href{{{data['paperLink']}}}{{\\underline{{this paper}}}}")
                    latex_content.append(f"        \\resumeItem{{{accomplishment}}}")
                latex_content.append(f"    \\resumeItemListEnd")
            latex_content.append("")
    
    return '\n'.join(latex_content)

def generate_projects_latex(data_dir):
    project_files = glob.glob(os.path.join(data_dir, 'projects', '*.md'))
    project_files = [f for f in project_files if not f.endswith('_template.md')]
    
    latex_content = []
    for file_path in sorted(project_files):
        data = parse_frontmatter(file_path)
        if data:
            latex_content.append(f"    \\resumeProjectHeading")
            latex_content.append(f"        {{\\textbf{{{data['name']}}} $|$ \\emph{{{data['technologies']}}} $|$ \\footnotesize\\href{{{data['link']}}}{{{data['link']}}}}}{{}}")
            
            if 'accomplishments' in data and data['accomplishments']:
                latex_content.append(f"        \\resumeItemListStart")
                for accomplishment in data['accomplishments']:
                    latex_content.append(f"        \\resumeItem{{{accomplishment}}}")
                latex_content.append(f"        \\resumeItemListEnd")
    
    return '\n'.join(latex_content)

def generate_skills_latex(data_dir):
    skills_files = glob.glob(os.path.join(data_dir, 'skills', '*.md'))
    skills_files = [f for f in skills_files if not f.endswith('_template.md')]
    
    latex_content = []
    for file_path in sorted(skills_files):
        data = parse_frontmatter(file_path)
        if data:
            latex_content.append(f"    \\textbf{{{data['category']}}}{{: ")
            latex_content.append(f"    {data['skills']}")
            latex_content.append(f"    }} \\\\")
    
    return '\n'.join(latex_content)

def generate_achievements_latex(data_dir):
    achievement_files = glob.glob(os.path.join(data_dir, 'achievements', '*.md'))
    achievement_files = [f for f in achievement_files if not f.endswith('_template.md')]
    
    latex_content = []
    for file_path in sorted(achievement_files, key=lambda x: parse_frontmatter(x).get('year', ''), reverse=True):
        data = parse_frontmatter(file_path)
        if data:
            title = data['title']
            if 'location' in data:
                title += f", \\emph{{{data['location']}}}"
            title += f", {data['year']}"
            
            latex_content.append(f"        {title} & ")
            latex_content.append(f"            \\footnotesize\\href{{{data['link']}}}{{{data['link'].replace('_', '\\_')}}} \\\\")
    
    return '\n'.join(latex_content)

def main():
    script_dir = Path(__file__).parent
    data_dir = script_dir / 'resume-data'
    
    print("% Generated Education Section")
    print(generate_education_latex(data_dir))
    print()
    
    print("% Generated Experience Section") 
    print(generate_experience_latex(data_dir))
    print()
    
    print("% Generated Projects Section")
    print(generate_projects_latex(data_dir))
    print()
    
    print("% Generated Skills Section")
    print(generate_skills_latex(data_dir))
    print()
    
    print("% Generated Achievements Section")
    print(generate_achievements_latex(data_dir))

if __name__ == "__main__":
    main()
