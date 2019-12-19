pipeline {
  agent { 
    docker {
       image 'python' 
    }
  }
  stages {
    stage('clean') {
      steps {
          sh 'pyc ./'  
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
    stage('createAPK'){
      steps{
        sh './gradlew assembleRelease'  
      }
    }
  }
  post {
    always {            
      junit 'app/build/test-results/**/*.xml'
      androidLint canComputeNew: false, defaultEncoding: '', healthy: '', pattern: 'app/build/reports/**/*', unHealthy: ''
      archiveArtifacts 'app/build/outputs/apk/**/*.apk'
      dir('app/build/test-results'){ 
        deleteDir()
      }
      
    }
  }
} 