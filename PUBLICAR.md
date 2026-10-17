# Cómo publicar (no ejecutado)
1. `gh auth login` (Francisco)
2. Sustituir S4ntos23 en README.md por el usuario de GitHub.
3. `gh repo create sample-size-calculator --public --source=. --push`
4. Pages: `gh api -X POST repos/S4ntos23/sample-size-calculator/pages -f 'source[branch]=main' -f 'source[path]=/'`
   (o Settings → Pages → Deploy from branch: main, / (root)). index.html = calculadora; .nojekyll incluido.
