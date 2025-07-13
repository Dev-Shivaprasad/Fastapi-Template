# Dependencies

# uses [PNPM](https://pnpm.io/)
![PNPM](https://pnpm.io/img/pnpm-no-name-with-frame.svg)

1. pnpm create vite {appname} --template react-ts
1. `pnpm add tailwindcss @tailwindcss/vite`
---
>vite.config.ts
3. `import { defineConfig } from 'vite'`  
  --> ` import tailwindcss from '@tailwindcss/vite'`  
`export default defineConfig({`  
  `plugins: [`  
   --> ` tailwindcss(),`  
  `],`  
`})`
---
>app.css  
4. `@import "tailwindcss";`
---
5. `pnpm add motion jwtdecode dotenv lucide-react clsx tailwind-merge axios`