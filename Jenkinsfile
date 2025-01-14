pipeline {
    agent {
        label 'docker'
    }
    
    environment {
        DOCKER_CREDENTIALS_ID = 'docker'
        BUILD_TAG = "${BUILD_NUMBER}"
        FE_IMAGE = "razielrey/domain-monitor-fe"
        BE_IMAGE = "razielrey/domain-monitor-be"
    }
    
    stages {
        stage('Clean Workspace') {
            steps {
                cleanWs()
                echo 'Workspace cleaned'
                script {
                    sh"""
                        if [ \$(sudo docker ps -aq) ]; then
                            sudo docker rm -f \$(sudo docker ps -aq)
                        else
                            echo "No containers to remove"
                        fi
                        # Remove old images
                        sudo docker image prune -f
                        # Create network or ignore if exists
                        sudo docker network create test-network || true
                    """
                }
                echo 'Docker containers removed and network created'
            }
        }
        
        stage('Clone Repository') {
            steps {
                dir('MonitoringApp') {
                    script {
                        git branch: 'FE-BE_Exercise', url: 'https://github.com/RazielRey/DevOpsCourse.git'
                        COMMIT_ID = sh(script: 'git rev-parse HEAD', returnStdout: true).trim().take(5)
                    }
                }
            }
        }
        
        stage('Build Docker Images') {
            parallel {
                stage('Build Frontend') {
                    steps {
                        dir('MonitoringApp/DevOpsCourse/app/FE') {
                            script {
                                sh """
                                    sudo docker build -t ${FE_IMAGE}:${BUILD_TAG} .
                                    sudo docker tag ${FE_IMAGE}:${BUILD_TAG} ${FE_IMAGE}:latest
                                """
                            }
                        }
                    }
                }
                
                stage('Build Backend') {
                    steps {
                        dir('MonitoringApp/DevOpsCourse/app/BE') {
                            script {
                                sh """
                                    sudo docker build -t ${BE_IMAGE}:${BUILD_TAG} .
                                    sudo docker tag ${BE_IMAGE}:${BUILD_TAG} ${BE_IMAGE}:latest
                                """
                            }
                        }
                    }
                }
            }
        }
        
        stage('Start Application Stack') {
            steps {
                script {
                    sh """
                        # Start Backend
                        sudo docker run -d --network test-network \
                            --name be-app-${BUILD_TAG} \
                            -p 5001:5001 \
                            -e PORT=5001 \
                            ${BE_IMAGE}:${BUILD_TAG}
                        
                        # Wait for backend to be ready
                        sleep 5
                        
                        # Start Frontend with link to Backend
                        sudo docker run -d --network test-network \
                            --name fe-app-${BUILD_TAG} \
                            -p 8080:8080 \
                            -e PORT=8080 \
                            -e BE_URL=http://be-app-${BUILD_TAG}:5001 \
                            ${FE_IMAGE}:${BUILD_TAG}
                        
                        # Wait for frontend to be ready
                        sleep 10
                        
                        # Verify both containers are running
                        sudo docker ps | grep app-${BUILD_TAG}
                    """
                }
            }
        }
        
        stage('Health Check') {
            steps {
                script {
                    sh """
                        # Check if Backend is responding
                        for i in \$(seq 1 6); do
                            if curl -f http://localhost:5001/health 2>/dev/null; then
                                echo "Backend is healthy"
                                break
                            fi
                            if [ \$i -eq 6 ]; then
                                echo "Backend health check failed"
                                exit 1
                            fi
                            sleep 5
                        done

                        # Check if Frontend is responding
                        for i in \$(seq 1 6); do
                            if curl -f http://localhost:8080/health 2>/dev/null; then
                                echo "Frontend is healthy"
                                break
                            fi
                            if [ \$i -eq 6 ]; then
                                echo "Frontend health check failed"
                                exit 1
                            fi
                            sleep 5
                        done
                    """
                }
            }
        }
        
        stage('Selenium Test') {
            steps {
                script {
                    sh """
                        # Run selenium container in the same network
                        sudo docker run --network test-network \
                            -d \
                            --name selenium-test \
                            -e APP_URL=http://fe-app-${BUILD_TAG}:8080 \
                            razielrey/selenium-tests:latest \
                            tail -f /dev/null
                            
                        sleep 5  # Wait for container to be ready
                        
                        # Run tests
                        if ! sudo docker exec selenium-test python3 run_tests.py; then
                            echo "Selenium tests failed"
                            exit 1
                        fi
                    """
                }
            }
        }
    }
    
    post {
        success {
            script {
                withCredentials([usernamePassword(credentialsId: 'docker', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh """
                        echo ${DOCKER_PASS} | sudo docker login -u ${DOCKER_USER} --password-stdin
                        
                        # Push Frontend images
                        sudo docker push ${FE_IMAGE}:${BUILD_TAG}
                        sudo docker push ${FE_IMAGE}:latest
                        
                        # Push Backend images
                        sudo docker push ${BE_IMAGE}:${BUILD_TAG}
                        sudo docker push ${BE_IMAGE}:latest
                    """
                }
            }
        }
        
        always {
            sh """
                # Clean up containers
                sudo docker rm -f be-app-${BUILD_TAG} fe-app-${BUILD_TAG} selenium-test || true
                sudo docker network rm test-network || true
                
                # Clean up dangling images
                sudo docker image prune -f
            """
        }
    }
}
