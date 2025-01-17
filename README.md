### **Description**
The `CQ Plugin Starter` is a CLI tool that helps you quickly create CloudQuery plugin templates. It fetches a pre-defined `cookiecutter` template, collects user inputs, and sets up your project directory automatically.

With just one command, you can:
- Clone the Ctwilio-internal/cloudquery-plugins repository.
- Fetch the cookiecutter template.
- Set up a feature branch.
- Customize the template with your inputs.
- Refactor and create your new plugin directory.

### **How to Use**
Run the following command to download and execute the automation script:

```bash
curl -L -o cq-plugin-starter https://github.com/markgraziano-twlo/cloudquery-cookiecutter/releases/download/v1.0.0/cq-plugin-starter && chmod +x cq-plugin-starter && ./cq-plugin-starter
```

### **Changelog**
- **v1.0.0**
  - Initial release of the `CQ Plugin Starter`.
  - Automates CloudQuery plugin template creation and setup.
