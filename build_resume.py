#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path
from parse_data import (
    generate_education_latex,
    generate_experience_latex,
    generate_projects_latex,
    generate_skills_latex,
    generate_achievements_latex
)

def build_resume():
    script_dir = Path(__file__).parent
    data_dir = script_dir / 'resume-data'
    template_file = script_dir / 'template' / 'resume_template.tex'
    output_file = script_dir / 'RyanBatubaraResume.tex'
    
    # Read the template
    with open(template_file, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    # Generate content for each section
    education_content = generate_education_latex(data_dir)
    experience_content = generate_experience_latex(data_dir)
    projects_content = generate_projects_latex(data_dir)
    skills_content = generate_skills_latex(data_dir)
    achievements_content = generate_achievements_latex(data_dir)
    
    # Replace placeholders
    final_content = template_content\
        .replace('% EDUCATION_PLACEHOLDER', education_content)
    final_content = final_content\
        .replace('% EXPERIENCE_PLACEHOLDER', experience_content)
    final_content = final_content\
        .replace('% PROJECTS_PLACEHOLDER', projects_content)
    final_content = final_content\
        .replace('% SKILLS_PLACEHOLDER', skills_content)
    final_content = final_content\
        .replace('% ACHIEVEMENTS_PLACEHOLDER', achievements_content)
    
    # Write the final resume
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    print(f"✅ Resume generated successfully: {output_file}")
    
    # Compile to PDF
    try:
        result = subprocess.run(['pdflatex', str(output_file)], 
                              capture_output=True, text=True, cwd=script_dir)
        if result.returncode == 0:
            print(f"✅ PDF compiled successfully: {script_dir / 'RyanBatubaraResume.pdf'}")
        else:
            print(f"❌ PDF compilation failed:")
            print(result.stderr)
    except FileNotFoundError:
        print("""⚠️  pdflatex not found. LaTeX file generated but PDF compilation skipped.""")
        print("   Install LaTeX to enable PDF generation.")

if __name__ == "__main__":
    build_resume()
