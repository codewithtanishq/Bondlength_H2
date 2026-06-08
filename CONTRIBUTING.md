# Contributing to Quantum H₂ PES Simulation

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this project.

## 🎯 How to Contribute

### Reporting Bugs
- **Check existing issues** first to avoid duplicates
- **Use a clear title** describing the problem
- **Include reproduction steps** and expected vs. actual behavior
- **Add environment details**: OS, Python version, dependency versions
- **Attach error logs** if applicable

### Suggesting Enhancements
- **Use a descriptive title** starting with "Feature:" or "Enhancement:"
- **Describe the use case** and expected benefit
- **Provide examples** of how it would be used
- **Consider performance impact** and dependencies

### Submitting Code Changes

#### 1. Fork & Clone
```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/quantum-h2-pes.git
cd quantum-h2-pes
git checkout -b feature/your-feature-name
```

#### 2. Set Up Development Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### 3. Make Your Changes
- **Follow the existing code style**
- **Add docstrings** to functions and classes
- **Write comments** for complex logic
- **Test your changes** thoroughly
- **Update documentation** if needed

#### 4. Code Style Guidelines

**Python Style**: Follow PEP 8
```python
# Good
def calculate_energy(distance, basis_set="sto-3g"):
    """Calculate molecular energy at given distance.
    
    Args:
        distance (float): Bond length in Ångströms
        basis_set (str): Quantum basis set to use
    
    Returns:
        float: Ground state energy in Hartree
    """
    pass

# Bad
def calc_E(d,b="sto-3g"):
    pass
```

**Comments**: Clear and meaningful
```python
# Calculate overlap matrix using given basis
overlap_matrix = calculate_overlap(basis_set)  # Good

# DO STUFF
result = do_something()  # Bad
```

#### 5. Run Tests & Validation
```bash
# Check individual phases
python src/phase0_baseline.py

# Run all phases
python demo.py --phase 0

# Check imports
python -m py_compile src/your_modified_file.py
```

#### 6. Commit & Push
```bash
# Commit with descriptive message
git add .
git commit -m "feat: add support for custom ansatz implementation

- Implement new CustomAnsatz class
- Add configuration options in config.py
- Update Phase 1 to use custom ansatz
- Add unit tests for new functionality"

# Push to your fork
git push origin feature/your-feature-name
```

#### 7. Create Pull Request
- **Title**: Start with type: `feat:`, `fix:`, `docs:`, `refactor:`, `perf:`
- **Description**: Link to related issues, describe changes
- **Screenshots**: Include if UI/visualization changes
- **Tests**: Verify all phases run without errors

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation change
- `style`: Code style change (formatting, etc.)
- `refactor`: Code restructuring without feature change
- `perf`: Performance improvement
- `test`: Test addition/modification
- `chore`: Build process, dependencies, etc.

**Examples**:
```
feat(phase1): implement UCCSD ansatz optimization

- Replace RealAmplitudes with UCCSD for better convergence
- Update optimizer to use SLSQP
- Improve convergence criteria detection

Closes #123
```

## 📋 Review Process

1. **Automated Checks**: Tests and linting run automatically
2. **Code Review**: Maintainers review for:
   - Code quality and consistency
   - Correctness of quantum algorithms
   - Documentation completeness
   - Performance implications
3. **Requests**: We may request changes; please update your PR
4. **Merge**: Once approved, changes are merged to main

## 🧪 Testing Guidelines

### Phase Testing
```bash
# Test individual phase
python src/phase0_baseline.py
python src/phase1_vqe.py --ansatz uccsd --max_iter 100

# Test with custom configuration
export PHASE_TEST=1
python src/phase2_noise.py
```

### Result Validation
- Verify output files are created in `results/`
- Check CSV files have expected headers
- Verify PNG plots are generated without errors
- Compare energy values against reference results

## 📚 Documentation

### Code Comments
- **Use docstrings** for functions, classes, modules
- **Explain "why"**, not just "what"
- **Include examples** in complex functions
- **Reference papers** for quantum algorithms

### README Updates
- Update if you add new features
- Add examples if introducing new functionality
- Update phase descriptions if modified
- Keep troubleshooting section current

### CHANGELOG
When making significant changes:
```markdown
## [1.1.0] - YYYY-MM-DD
### Added
- New feature description

### Fixed
- Bug fix description

### Changed
- Breaking change description
```

## 🔑 Key Areas for Contribution

### Easy (Good for First-Timers)
- [ ] Improve documentation and docstrings
- [ ] Add examples to README
- [ ] Fix typos in code comments
- [ ] Enhance error messages
- [ ] Add configuration options

### Medium
- [ ] Add new basis sets (6-31G*, aug-cc-pVDZ, etc.)
- [ ] Implement new noise models
- [ ] Add visualization improvements
- [ ] Performance optimizations
- [ ] Enhanced error handling

### Advanced
- [ ] New quantum ansätze implementations
- [ ] Hardware-specific optimizations
- [ ] Hybrid quantum-classical algorithms
- [ ] Support for larger molecules (Li₂, H₂O)
- [ ] Integration with real quantum hardware

## 🚀 Development Workflow

```
1. Create issue or find existing one
   ↓
2. Fork repository
   ↓
3. Create feature branch
   ↓
4. Make changes & commit
   ↓
5. Push to fork
   ↓
6. Create pull request
   ↓
7. Address review feedback
   ↓
8. Merge to main
```

## 📞 Questions?

- **GitHub Issues**: Ask questions in issues
- **GitHub Discussions**: Use for general questions
- **Email**: Contact maintainers directly

## ⚖️ Code of Conduct

Please be respectful and professional:
- Be inclusive and welcoming
- Respect different perspectives
- Keep discussions focused on the topic
- Report inappropriate behavior

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to advancing quantum computing education! 🎉**
