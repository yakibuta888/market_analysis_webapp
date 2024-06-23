# syntax=docker/dockerfile:1.4.1
FROM node:18.20-bullseye as builder

ARG WORKDIR
WORKDIR ${WORKDIR}

# Install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy source files
COPY . .

# Build the application
RUN npm run build

# Production stage
FROM node:18.20-bullseye as production

ARG WORKDIR
WORKDIR ${WORKDIR}

# Create the user
ARG USERNAME
ARG HOMEDIR
ARG USERID
ARG GROUPID
RUN usermod -u 999 node && groupmod -g 999 node
RUN <<-EOF
	echo "Create User = ${USERID}. Group = ${GROUPID}"
	groupadd -g ${GROUPID} ${USERNAME}
	useradd -m -s /bin/bash -d ${HOMEDIR} -k /etc/skel -u ${USERID} -g ${GROUPID} ${USERNAME}
	echo ${USERNAME} ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/${USERNAME}
	chmod 0440 /etc/sudoers.d/${USERNAME}
EOF
USER ${USERNAME}

# Copy built files from the build stage
COPY --from=builder ${WORKDIR}/dist ./dist
COPY --from=builder ${WORKDIR}/package.json ./
COPY --from=builder ${WORKDIR}/node_modules ./node_modules

# Expose the port the app runs on
EXPOSE 8080

# Start the application
CMD ["npm", "start"]
