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
    stage('Unit Test'){
      parallel {
        stage('pytest'){
          steps{
            dir('binary') {
              script {
                try {
                  sh sh 'python -m pytest tests/ --junitxml test-reports/report-$BUILD_NUMBER.xml'
                } catch (Exception e) {
                  echo e.getMessage()
                  echo "Lint failed"
                }
              }  
            }     
          }
        }
        stage('doctest'){
          steps{
            dir('binary') {
              script {
                try {
                  sh 'python -m doctest -v binary.py'
                } catch (Exception e) {
                  echo e.getMessage()
                  echo "test failed"
                }
              }   
            }    
          }   
        }
      }
    }
  }
  post {
    always {            
      archiveArtifacts 'test-reports/*'
      dir('test-reports'){ 
        deleteDir()
      }      
    }
  }
} 