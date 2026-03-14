# #################################################################### #
#                                                                      #
# builder image                                                        #
#                                                                      #
# #################################################################### #
FROM node@sha256:f4769ca6eeb6ebbd15eb9c8233afed856e437b75f486f7fccaa81d7c8ad56007 AS build

RUN npm install -g pnpm@10.30.3

WORKDIR /app

COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
RUN pnpm install --frozen-lockfile

COPY . .
RUN pnpm run build

# #################################################################### #
#                                                                      #
# prod image                                                           #
#                                                                      #
# #################################################################### #
FROM node@sha256:f4769ca6eeb6ebbd15eb9c8233afed856e437b75f486f7fccaa81d7c8ad56007 AS prod

ENV PORT=3000
ENV HOST=0.0.0.0

WORKDIR /app

COPY --from=build /app/.output ./.output

EXPOSE ${PORT}

CMD [ "node", ".output/server/index.mjs" ]