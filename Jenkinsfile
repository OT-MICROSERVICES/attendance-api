@Library('cicid-shared-lib@notification') _
def cipipeline = new opstree.ci.templates.python_ci.python_ci()

node {
  cipipeline.call([
    enable_jenkins_build_param_override: true,

    // WORKSPACE MANAGEMENT
    clean_workspace: true,
    ignore_clean_workspace_failure: true,
    delete_dirs: false,
    clean_when_build_aborted: true,
    clean_when_build_failed: true,
    clean_when_not_built: true,
    clean_when_build_succeed: true,
    clean_when_build_unstable: true,

    // VCS MANAGEMENT
    repo_https_url: "https://github.com/ayush090909/attendance-api.git",
    repo_ssh_url: "https://github.com/ayush090909/attendance-api.git",
    repo_branch: "main",
    repo_url_type: "http",
    jenkins_git_creds_id: "github-cred",
    source_code_path: "",

    // Dependency Scanning
    dependency_check: false,
    dependency_scan_tool: "owasp",
    owasp_project_name: "owasp",
    owasp_report_publish: true,
    owasp_report_format: "html",
    fail_job_if_dependency_returned_exception: true,

    // Creds Scanning
    gitleaks_check: false,
    fail_job_if_leak_detected: false,
    gitleaks_report_format: "json",
    gitleaks_report_jenkins_publish: true,

    // Code Build
    perform_code_build: false,
    build_tool: "maven",
    pom_location: " ",

    // Unit Testing
    unit_testing_check: false,
    fail_job_if_unit_issue_detected: false,
    unit_test_reports_path: "*/target/surefire-reports/*.xml",
    findbugs_test_report_path: "*/target/findbugs/*.xml",
    withmaven_globaltool_jdk: "",
    withmaven_globaltool_maven: "",
    mvn_settings_path: "settings.xml",

    // Static Code Analysis
    codebase_to_scan_directory: "**",
    static_code_analysis_check: false,
    path_to_sonar_properties: "sonar.properties",
    fail_job_if_analysis_returned_exception: false,
    jenkins_sonarqube_token_creds_id: "sonar-token",

    // Build Dockerfile
    perform_build_dockerfile: true,
    image_name: "attendence-api",
    dockerfile_location: "/Dockerfile",
    dockerfile_context: "",
    codeartifact_dependency: false,

    // Image scanning
    image_scanning_check: false,
    image_tag: "latest",
    scan_severity: "CRITICAL",
    image_scanning_report_publish: true,

    // Image size validator
    image_size_validator_check: false,
    max_allowed_image_size: 100,
    fail_job_if_validation_fail: false,

    // Publish Artifact (Docker Image)
    artifact_publish_check: true,
    artifact_destination_type: "harbor",
    jenkins_aws_credentials_id: "aws-rajat",
    docker_image_name: "attendence-api",
    ecr_repo_name: "",
    ecr_region: "ap-south-1",
    account_id: "",

    // Harbor Specific Parameters
    harbor_url: "registry.ldc.opstree.dev",
    harbor_project: "ot-microservices",
    harbor_credentials_id: "harbor-creds",

    // Dockle scanning
    dockle_scan_check: 'false',
    dockle_report_publish: 'true',

    // Hadolint Dockerfile scan
    hadolint_scan_check: 'false',
    hadolint_report_publish: 'true',
    fail_job_on_hadolint_error: 'false',
    dockerfile_context: '',
    repo_dir: '',

    // JIRA
    jenkins_jira_url_env_name: "JIRA_URL",
    jenkins_jira_creds_id: "jira-ticket-update-credentials",
    fail_job_if_jira_operation_failed: true,
    enable_jira: false,
    enable_buildlogurl_in_jiracomment: true,

    // Trigger CD Pipeline
    enable_trigger_cd_pipeline: false,
    image_name_build_param: "image_name",
    image_tag_build_param: "image_tag",
    enable_jira_build_param: "enable_jira",
    jira_ticket_id_build_param: "jira_ticket_id",
    trigger_cd_pipeline_path: "",

    // ✅ Slack Notification (Hardcoded for Testing)
    notification_enabled: true,
    notification_channel: "slack",
    notification_mode: "custom",  // custom to use webhook directly
    webhook_url: "https://hooks.slack.com/services/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",
    resultStatus: "started",
    instanceId: "instance-1234",
    action: "deploy",
    slack_channel: "#general"
  ])
}
