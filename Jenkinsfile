pipeline {
  agent { 
    docker {
       image 'python' 
    }
  }
  stages {
    stage('clean') {
      steps {
          sh './pyc.sh ./'  
      }
    }
    stage('build') {
      steps {
          sh 'pip install -r ./requirements.txt'
      }
    }
    stage('Unit Test'){
      parallel {
        stage('pytest'){
          steps{
            dir('binary') {
              script {
                try {
                  sh 'python -m pytest tests/ --junitxml test-reports/report-$BUILD_NUMBER.xml'
                } catch (Exception e) {
                  echo e.getMessage()
                  echo "Lint failed"
                }
              }  
            }     
          }
        }
      }
    }
    stage('juint'){
      steps {
        junit 'binary/test-reports/*.xml'
      }
    }
    stage('Sonarqube') {
      environment {
        scannerHome = tool 'SonarQubeScanner'
      }
      steps {
        withSonarQubeEnv('sonarqube') {
          sh "${scannerHome}/bin/sonar-scanner"
        }
        timeout(time: 30, unit: 'MINUTES') {
          waitForQualityGate abortPipeline: true
        }
      }
    }
  }
  post {
    always {            
      archiveArtifacts 'binary/test-reports/*.xml'
      dir('binary/test-reports'){ 
        deleteDir()
      }      
    }
  }
} 