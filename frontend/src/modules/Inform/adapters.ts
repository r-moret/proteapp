import { EditInformSchema, InformInfoSchema, InformSchema } from './declarations'

export const InformAdapter = (input: any) => InformSchema.parse(input)
export const InformInfoAdapter = (input: any) => InformInfoSchema.parse(input)
export const EditInformAdapter = (input: any) => EditInformSchema.parse(input)
