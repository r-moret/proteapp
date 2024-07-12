import { AnimalSchema } from './declarations'

export const AnimalAdapter = (input: any) => AnimalSchema.parse(input)
