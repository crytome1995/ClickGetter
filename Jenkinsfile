#!/usr/bin/env groovy


def label="clickgetter-${UUID.randomUUID().toString()}"
def gitCommit 
def repoName = "ethanlebioda/clickcounter"
def dev = "dev"
def main = "main"
def argoApp = "clickgetter-"
def appWaitTimeout = 600
def argocdServer = "argocd-server.argocd.svc.cluster.local"
podTemplate(label: label, 
    containers: [
        containerTemplate(name: 'python', image: 'python:3.9.6-slim',ttyEnabled: true, privileged: true, command: 'cat', envVars: [envVar(key: 'E2E_HOST', value: 'http://clickgetter.control.clickthebutton.click')]),
        containerTemplate(name: 'dind', image: 'docker:20-dind',privileged: true, envVars: [envVar(key: 'DOCKER_TLS_CERTDIR', value: '')]),
        containerTemplate(name: 'argo', image: 'ethanlebioda/argocli-sleep:1.0.0',ttyEnabled: true)
    ])

{
  timeout(time: 4, unit: 'HOURS') {
    node(label) {

      stage ("Checkout SCM") {
        def scmVars = checkout scm
        def lastCommit = sh script: 'git log -1 --pretty=%B', returnStdout: true
        echo ("last commit: ${lastCommit}")
        echo ("commit HASH: ${scmVars.GIT_COMMIT}")
        gitCommit = scmVars.GIT_COMMIT
      }

      stage('Test project') {
        container('python') {
            sh 'pip3 install -r requirements.txt'
            def passed = sh script: 'pytest --ignore=click_getter/e2e', returnStatus: true
            if (passed != 0) {
                  currentBuild.result = 'ABORTED'
                  error('Failed unit tests!')
            }
          }
        }

      stage('Build Project') {
        container('dind') {
          def buildStatus = sh script: "docker build -t ${repoName} .", returnStatus: true
          if (buildStatus != 0) {
            currentBuild.result = 'ABORTED'
            error('Failed to build image!')
          }
          withCredentials([string(credentialsId: 'DOCKERHUB_USERNAME', variable: 'DOCKERHUB_USERNAME'),
                            string(credentialsId: 'DOCKERHUB_ACCESS_TOKEN', variable: 'DOCKERHUB_ACCESS_TOKEN')]) {
            sh 'docker login -u $DOCKERHUB_USERNAME -p $DOCKERHUB_ACCESS_TOKEN'
            def imageToPush = "${repoName}:${gitCommit}"
            sh "docker tag  ${repoName} ${imageToPush}"
            echo "Pushing image ${imageToPush}"
            def pushStatus = sh script: "docker push ${imageToPush}", returnStatus: true
            if (pushStatus != 0) {
              currentBuild.result = 'ABORTED'
              error('Failed to push image!')
            }
          }
        }
      }

      stage('release to dev') {
        withCredentials([usernamePassword(credentialsId: 'GITHUB_JENKINS', usernameVariable: 'GIT_USERNAME', passwordVariable: 'GIT_TOKEN')]) {
          sh 'chmod +x scripts/release.sh'
          def releasedDev = sh script: "scripts/release.sh ${dev} ${gitCommit}", returnStatus: true
          if (releasedDev != 0) {
            currentBuild.result = 'ABORTED'
            error('Failed to release to dev!')
          }
          container('argo') {
            withCredentials([usernamePassword(credentialsId: 'ARGOCD', usernameVariable: 'ARGOCD_USERNAME', passwordVariable: 'ARGOCD_PASSWORD')]) {
              sh 'argocd login argocd-server.argocd.svc.cluster.local --insecure --plaintext --username $ARGOCD_USERNAME --password $ARGOCD_PASSWORD'
              sh "argocd app sync ${argoApp}${dev}"
              sh "argocd app wait ${argoApp}${dev} --timeout ${appWaitTimeout}"
            }
          }
        }
      }

      stage('E2E test') {
        container('python') {
          sh 'pip3 install -r click_getter/e2e/requirements.txt'
          def uiTestStatus = sh script:'pytest click_getter/e2e/', returnStatus: true
          if (uiTestStatus != 0) {
            currentBuild.result = 'ABORTED'
            error('End to end tests failed!')
          }
        }
      }

      stage('release to prod') {
        withCredentials([usernamePassword(credentialsId: 'GITHUB_JENKINS', usernameVariable: 'GIT_USERNAME', passwordVariable: 'GIT_TOKEN')]) {
          def releaseProd = sh script: "scripts/release.sh ${main} ${gitCommit}", returnStatus: true
          if (releaseProd != 0) {
            currentBuild.result = 'ABORTED'
            error('Failed to release to prod!')
          }
        }
        container('argo') {
          withCredentials([usernamePassword(credentialsId: 'ARGOCD', usernameVariable: 'ARGOCD_USERNAME', passwordVariable: 'ARGOCD_PASSWORD')]) {
            sh 'argocd login argocd-server.argocd.svc.cluster.local --insecure --plaintext --username $ARGOCD_USERNAME --password $ARGOCD_PASSWORD'
            sh "argocd app sync ${argoApp}prod"
            sh "argocd app wait ${argoApp}prod --timeout ${appWaitTimeout}"
          }
        }
      }
    }
  }
}