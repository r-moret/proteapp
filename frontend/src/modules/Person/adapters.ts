import { PersonSchema, EditPersonSchema } from './declarations'

export const PersonAdapter = (input: any) => PersonSchema.parse(input)
export const EditPersonAdapter = (input: any) => EditPersonSchema.parse(input)
