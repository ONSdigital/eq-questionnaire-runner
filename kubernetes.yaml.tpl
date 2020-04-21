# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

apiVersion: apps/v1
kind: Deployment
metadata:
  name: eq-author-runner
  labels:
    app: eq-author-runner
spec:
  replicas: 1
  selector:
    matchLabels:
      app: eq-author-runner
  template:
    metadata:
      labels:
        app: eq-author-runner
    spec:
      containers:
      - name: eq-author-runner
        image: eu.gcr.io/GOOGLE_CLOUD_PROJECT/eq-author-runner:COMMIT_SHA
        ports:
        - containerPort: 5000
        env:
          - name: EQ_STORAGE_BACKEND
            valueFrom:
              secretKeyRef:
                name: author-runner-secrets
                key: EQ_STORAGE_BACKEND
          - name: EQ_REDIS_HOST
            valueFrom:
              secretKeyRef:
                name: author-runner-secrets
                key: EQ_REDIS_HOST
          - name: EQ_REDIS_PORT
            valueFrom:
              secretKeyRef:
                name: author-runner-secrets
                key: EQ_REDIS_PORT
          - name: EQ_SUBMITTED_RESPONSES_TABLE_NAME
            valueFrom:
              secretKeyRef:
                name: author-runner-secrets
                key: EQ_SUBMITTED_RESPONSES_TABLE_NAME
          - name: EQ_QUESTIONNAIRE_STATE_TABLE_NAME
            valueFrom:
              secretKeyRef:
                name: author-runner-secrets
                key: EQ_QUESTIONNAIRE_STATE_TABLE_NAME
          - name: EQ_SESSION_TABLE_NAME
            valueFrom:
              secretKeyRef:
                name: author-runner-secrets
                key: EQ_SESSION_TABLE_NAME
          - name: EQ_USED_JTI_CLAIM_TABLE_NAME
            valueFrom:
              secretKeyRef:
                name: author-runner-secrets
                key: EQ_USED_JTI_CLAIM_TABLE_NAME
          - name: EQ_SECRETS_FILE
            valueFrom:
              secretKeyRef:
                name: author-runner-secrets
                key: EQ_SECRETS_FILE
          - name: EQ_KEYS_FILE
            valueFrom:
              secretKeyRef:
                name: author-runner-secrets
                key: EQ_KEYS_FILE
          - name: EQ_SUBMISSION_BACKEND
            valueFrom:
              secretKeyRef:
                name: author-runner-secrets
                key: EQ_SUBMISSION_BACKEND
          - name: EQ_SESSION_TIMEOUT_SECONDS
            valueFrom:
              secretKeyRef:
                name: author-runner-secrets
                key: EQ_SESSION_TIMEOUT_SECONDS
          - name: EQ_ENABLE_SECURE_SESSION_COOKIE
            valueFrom:
              secretKeyRef:
                name: author-runner-secrets
                key: EQ_ENABLE_SECURE_SESSION_COOKIE


---
kind: Service
apiVersion: v1
metadata:
  name: eq-author-runner
spec:
  selector:
    app: eq-author-runner
  ports:
  - protocol: TCP
    port: 80
    targetPort: 5000
  type: LoadBalancer