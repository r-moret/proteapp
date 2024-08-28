import {
  AdoptionInfoSchema,
  AdoptionSchema,
  EditMonitoringSchema,
  EditAdoptionSchema
} from './declarations'
import { ImageAdapter } from '@/utils'

export const AdoptionInfoAdapter = (input: any) =>
  ImageAdapter(AdoptionInfoSchema.parse(input), 'animal.image')
export const AdoptionAdapter = (input: any) =>
  ImageAdapter(AdoptionSchema.parse(input), 'animal.image')
export const EditMonitoringAdapter = (input: any) => EditMonitoringSchema.parse(input)
export const EditAdoptionAdapter = (input: any) => EditAdoptionSchema.parse(input)
