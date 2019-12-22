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
    stage('coverage'){
      steps{
        dir('binary/test-reports') {
          script {
            try {
              sh 'coverage erase'
              sh 'coverage run -m unittest discover -s ../tests'
              sh 'coverage xml -i'
            } catch (Exception e) {
              echo e.getMessage()
              echo "coverage failed"
            }
          } 
        }    
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